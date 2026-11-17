from .domain import ancestors, suggestions
from .storage import single


def inbox(store, query):
    month = single(query, 'month')
    rows = [message for message in store.table('messages')
            if month is None or message['month'] == month]
    return {'messages': [dict(message, hints=suggestions(store,message['text'])) for message in rows]}


def review(store, query):
    version = single(query, 'version', 'v1')
    counts = {}
    for row in store.table('labels'):
        if row['version'] != version:
            continue
        for label in set(row['labels']):
            for expanded in [label, *ancestors(store,label,version)]:
                counts[expanded] = counts.get(expanded,0) + 1
    return {'reviewer_label_counts': counts, 'unit': 'reviewer_decision',
            'release': store.table('releases')}


ROUTES = {'/api/inbox': inbox, '/api/review': review}
