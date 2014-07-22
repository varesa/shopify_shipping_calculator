import json

test_origin = "Villähde, Finland"

from shopify import Product
from .api_auth import create_session

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

    create_session()

    for item in items:
        prod = Product.find(item['product_id'])
        print(prod)
