import json

test_origin = "Villähde, Finland"

from shopify import Product

def calculate_shipping(requestjson):
    """
    :param requestjson: String with JSON-data that contains the request from shopify
    :type requestjson: str
    :return: Cost of shipping in cents
    :rtype: int
    """
    data = json.loads(requestjson)
    items = data['rate']['items']
    destination = data['rate']['destination']

    for item in items:
        prod = Product.find(id=item['product_id'])
        print(prod)
