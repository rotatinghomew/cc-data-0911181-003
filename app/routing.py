from .storage import DataError


def assign(store,journal,payload):
    message=store.find('messages',message=payload['message'])
    label=payload['label']
    owner=store.find('routing_rules',label=label)['owner']
    key=message['message']+':'+label
    with journal.transaction():
        existing=[row for row in journal.all('ticket') if row['ticket']==key]
        if existing:
            return existing[0]
        return journal.put('ticket',key,dict(ticket=key,message=message['message'],person=message['person'],
                                           label=label,owner=owner,status='open'))
