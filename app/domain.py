from .storage import DataError


def ancestors(store,label,version):
    nodes = {row['label']:row for row in store.select('taxonomy',version=version)}
    if label not in nodes:
        raise DataError('unknown label or taxonomy version')
    result=[]
    current=nodes[label].get('parent')
    while current is not None:
        if current in result or current not in nodes:
            raise DataError('invalid taxonomy')
        result.append(current)
        current=nodes[current].get('parent')
    return result


def suggestions(store,text):
    return [dict(label=rule['label'],rule=rule['rule'],status='candidate')
            for rule in store.table('hints') if rule['word'] in text]
