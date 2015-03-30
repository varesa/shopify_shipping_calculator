##
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#

from ..models import DBSession, ShippingCostLavatuote
from ..distance_helpers import find_closest
from ..exceptions import TooFarAwayException
from math import ceil


class CategoryLavatuotteet:

    destination = None
    ":type: str"
    items = None
    ":type: list of (Product, int)"

    def __init__(self, destination):
        self.items = []
        self.destination = destination

    def add_item(self, item, quantity):
        self.items.append((item, quantity))

    def has_items(self):
        return len(self.items) > 0

    def get_total(self):
        total = 0

        cost_lavametri_km = DBSession.query(ShippingCostLavatuote).first().cost_lavametri

        for item, quantity in self.items:
            distance = find_closest(item.locations, self.destination)['distance']
            if distance > item.km_raja:
                raise TooFarAwayException()
            units = ceil(quantity / item.maara_per_lavametri)

            total += units * distance * cost_lavametri_km

        return total