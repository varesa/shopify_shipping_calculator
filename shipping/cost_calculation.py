import json
from math import ceil

from shopify import Product as sf_Product
from .api_auth import create_session

from .distance_helpers import find_closest

from .models import DBSession, ShippingLocation
from .models import Product as db_Product


test_origin = json.dumps({
    'address1': '',
    'address2': '',
    'postal_code': '',
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

    # [{location, distance, bags}, {...}]
    bag_locations = []

    for item in items:
        handle = sf_Product.find(item['product_id']).handle
        product = DBSession.query(db_Product).filter_by(handle=handle)

        closest = find_closest(product.locations, destination)

        if product.type == 'säkki-1000l':
            found = False
            for bag_location in bag_locations:
                if bag_location['location'] == closest['location']:
                    found = True
                    bag_location['bags'] += item['quantity']

            if not found:
                bag_locations.append({'location': closest['location'], 'distance': closest['distance'], 'bags': item['quantity']})

        elif product.type == 'irtokuorma':
            pass

    total_price = 0

    for bag_location in bag_locations:
        total_price += price_per_km * bag_location['distance'] * ceil(bag_location['bags']/18)

    return total_price * 100