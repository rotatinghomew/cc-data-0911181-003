from .storage import DataError


def confirm(store,journal,payload):
    with journal.transaction():
        ticket=journal.get('ticket',payload['ticket'])
        if ticket['owner']!='curriculum':
            raise DataError('not a curriculum demand')
        row=dict(demand=ticket['ticket'],person=ticket['person'],label=ticket['label'],status='confirmed')
        journal.put('demand',row['demand'],row)
        people={item['person'] for item in journal.all('demand')
                if item['label']==ticket['label'] and item['status']=='confirmed'}
        rule=store.find('demand_rules',label=ticket['label'])
        return journal.put('candidate_course',ticket['label'],dict(label=ticket['label'],
                           confirmed_people=len(people),ready=len(people)>=rule['minimum_people']))
