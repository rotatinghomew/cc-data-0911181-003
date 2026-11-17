from pathlib import Path
import tempfile
import unittest
from app.journal import Journal
from app.storage import DataError,Store

DATA=Path(__file__).parents[1]/'data'


class BusinessChainTests(unittest.TestCase):
    def setUp(self):
        self.store=Store(DATA)
        self.journal=Journal()

    def tearDown(self):
        self.journal.close()

    def test_business_chain(self):
        self.exercise(self.store,self.journal)

    def test_rollback_on_failure(self):
        with self.assertRaises(DataError):
            with self.journal.transaction():
                self.journal.put('test','a',{'value':1})
                raise DataError('aborted')
        self.assertEqual(self.journal.all('test'),[])

    def test_restart_retains_business_records(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'workflow.sqlite3'
            journal=Journal(path)
            try:
                self.exercise(self.store,journal)
                before={kind[0] for kind in journal.connection.execute('SELECT DISTINCT kind FROM documents')}
                snapshot={kind:journal.all(kind) for kind in before}
            finally:
                journal.close()
            reopened=Journal(path)
            try:
                self.assertEqual(snapshot,{kind:reopened.all(kind) for kind in before})
            finally:
                reopened.close()

    def exercise(self,store,journal):
        from app import routing,course_demand,replies
        ticket=routing.assign(store,journal,dict(message='M000',label='photo'))
        routing.assign(store,journal,dict(message='M000',label='schedule'))
        course=course_demand.confirm(store,journal,dict(ticket=ticket['ticket']))
        self.assertFalse(course['ready'])
        reply=replies.resolve(store,journal,dict(ticket=ticket['ticket'],owner='curriculum',resolution='interest recorded'))
        self.assertEqual(reply['status'],'waiting')
        reply=replies.resolve(store,journal,dict(ticket='M000:schedule',owner='campus',resolution='night course pending'))
        self.assertEqual(reply['status'],'ready')
