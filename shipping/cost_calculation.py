import json
from math import ceil

from shopify import Product
from .api_auth import create_session

from .api_distance import get_distance

test_origin = json.dumps({
    'address1': '',
    'address2': '',
    'zip': '',
    'city': 'Villähde',
    'country': 'Finland'
})
price_per_km = 5.00

def calculate_shipping(requestjson):
    """
    :param requestjson: String with JSON-data that contains the request from shopify
    :type requestjson: str
    :return: Cost of shipping in cents
    :rtype: int
    """
    data = json.loads(requestjson)
    items = data['rate']['items']
    destination = json.dumps(data['rate']['destination'])

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

    total_price = 0

    for load in bag_loads:
        total_price += load[1] * price_per_km * get_distance(load[0], destination)