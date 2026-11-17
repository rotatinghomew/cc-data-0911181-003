from .storage import DataError


def resolve(store,journal,payload):
    with journal.transaction():
        ticket=journal.get('ticket',payload['ticket'])
        if ticket['owner']!=payload['owner']:
            raise DataError('wrong handling owner')
        ticket['status']='closed'
        ticket['resolution']=payload['resolution']
        journal.put('ticket',ticket['ticket'],ticket)
        siblings=[row for row in journal.all('ticket') if row['message']==ticket['message']]
        reply=dict(message=ticket['message'],status='ready' if all(row['status']=='closed' for row in siblings) else 'waiting',
                   resolutions=[dict(label=row['label'],resolution=row.get('resolution')) for row in siblings])
        return journal.put('reply',ticket['message'],reply)
