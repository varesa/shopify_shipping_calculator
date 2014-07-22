import json


def prettify_json(data):
    """
    Loads a JSON-string into an object and dumps it back into a string with a more human readable format.
    :param data: String or bytes object with JSON data
    :type data: bytes or str
    :return: Prettified JSON-string
    :rtype: str
    """
    if type(data) == type(b''):
        data = data.decode('utf-8')
    expanded = json.loads(data)
    return json.dumps(expanded, indent=4, separators=(',', ': '))