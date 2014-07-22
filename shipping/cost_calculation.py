import json
from math import ceil

from shopify import Product
from .api_auth import create_session

test_origin = "Villähde, Finland"

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

    bags = {}
    bag_loads = []

    for item in items:
        prod = Product.find(item['product_id'])

        if "suursäkki-1000l" in prod.tags:
            if test_origin not in bags.keys():
                bags[test_origin] = 0
            bags[test_origin] += item['quantity']

        for location, quantity in bags.items():
            bag_loads.append( (location, ceil(quantity/18)) )

    print(bag_loads)
