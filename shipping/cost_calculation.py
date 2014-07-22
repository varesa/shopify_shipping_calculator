import json

test_origin = "Villähde, Finland"

def calculate_shipping(requestjson):
    """
    :param requestjson: String with JSON-data that contains the request from shopify
    :type requestjson: str
    :return: Cost of shipping in cents
    :rtype: int
    """
    data = json.loads(requestjson)
    items = data['rates']['items']
    destination = data['rates']['destination']

    for item in items:
        print(item)
