#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


import json
from math import ceil

from shopify import Product as sf_Product
from shopify import Variant as sf_Variant
from ..api_auth import create_session

from .logic_sakit import CategorySakit
from .logic_irtotavara import CategoryIrtotavara
from .logic_muut import CategoryMuut

from ..models import DBSession
from ..models import Product as db_Product


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

    sakit = CategorySakit(destination)
    irtotavara = CategoryIrtotavara(destination)
    muut = CategoryMuut(destination)

    for item in items:
       	sf_product = sf_Product.find(item['product_id'])
        sf_variant = sf_Variant.find(item['variant_id']) 

        print(sf_variant.__dict__)

        handle = sf_product.handle + "-" + sf_variant.title
        product = DBSession.query(db_Product).filter_by(handle=handle).first()

        if product.type == 'sakki':
            sakit.add_item(product, item['quantity'])
        elif product.type == 'irtokuorma':
            irtotavara.add_item(product, item['quantity'])
        else:
            muut.add_item(product, item['quantity'])

    total_price = 0

    if sakit.has_items():
        total_price += sakit.get_total()

    if irtotavara.has_items():
        total_price += irtotavara.get_total()

    if muut.has_items():
        total_price += muut.get_total()

    return total_price * 100  # 1€ -> 100 cents
