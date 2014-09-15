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
bags_price_per_km = 5.00
irtokuorma_price_per_km = 4.1


def irtokuorma_hinta(distance, amount):
    if amount <= 18:
        return 60 + distance*irtokuorma_price_per_km
    elif amount <= 38:
        return 120 + distance*irtokuorma_price_per_km
    else:
        base = 120
        extra_tn = amount - 38
        extra = ceil(extra_tn/20)*20
        return base + extra + distance*irtokuorma_price_per_km


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
    irtokuormat = []

    for item in items:
        handle = sf_Product.find(item['product_id']).handle
        product = DBSession.query(db_Product).filter_by(handle=handle).first()

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
            irtokuormat.append({'location': closest['location'], 'distance': closest['distance'], 'amount': item['quantity']})

    total_price = 0

    for bag_location in bag_locations:
        print(str(bag_location['location']) + " km * " + str(bag_location['bags']) + "bags = " +
              str(bags_price_per_km * bag_location['distance'] * ceil(bag_location['bags']/18)))
        total_price += bags_price_per_km * bag_location['distance'] * ceil(bag_location['bags']/18)

    for irtokuorma in irtokuormat:
        print(str(irtokuorma['distance']) + " km * " + str(irtokuorma['amount']) + " tn = " +
              str(irtokuorma_hinta(irtokuorma['distance'], irtokuorma['amount'])))
        total_price += irtokuorma_hinta(irtokuorma['distance'], irtokuorma['amount'])

    return total_price * 100