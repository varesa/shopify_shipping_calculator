import json


def prettify_json(data):
    if type(data) == type(b''):
        data = data.decode('utf-8')
    expanded = json.loads(data)
    return json.dumps(expanded, indent=4, separators=(',', ': '))