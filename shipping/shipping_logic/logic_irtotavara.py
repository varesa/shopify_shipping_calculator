#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


from ..distance_helpers import find_closest
from ..models import DBSession, ShippingCostIrtotavara


HINTA_KUORIKATE_KIINTEA = 50

cost_nuppi = DBSession.query(ShippingCostIrtotavara).filter_by(name="nuppikuorma").first()
""":type: ShippingCostIrtotavara"""

NUPPI_MAX_PAINO = cost_nuppi.max_weight
NUPPI_LAHTOHINTA_KUORMA = cost_nuppi.base_cost

NUPPI_ALUE1_YLARAJA = cost_nuppi.range1_end
NUPPI_ALUE1_HINTA_KM = cost_nuppi.range1_cost

NUPPI_ALUE2_YLARAJA = cost_nuppi.range2_end
NUPPI_ALUE2_HINTA_KM = cost_nuppi.range2_cost

NUPPI_ALUE3_YLARAJA = None
NUPPI_ALUE3_HINTA_KM = cost_nuppi.range3_cost


cost_kasetti = DBSession.query(ShippingCostIrtotavara).filter_by(name="kasettikuorma").first()
""":type: ShippingCostIrtotavara"""

KASETTI_MAX_PAINO = cost_kasetti.max_weight
KASETTI_LAHTOHINTA_KUORMA = cost_kasetti.base_cost

KASETTI_ALUE1_YLARAJA = cost_kasetti.range1_end
KASETTI_ALUE1_HINTA_KM = cost_kasetti.range1_cost

KASETTI_ALUE2_YLARAJA = cost_kasetti.range2_end
KASETTI_ALUE2_HINTA_KM = cost_kasetti.range2_cost

KASETTI_ALUE3_YLARAJA = None
KASETTI_ALUE3_HINTA_KM = cost_kasetti.range3_cost


class CategoryIrtotavara():

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

    def laske_nuppi(self, distance):
        cost = NUPPI_LAHTOHINTA_KUORMA
        if distance < NUPPI_ALUE1_YLARAJA:
            cost += distance * NUPPI_ALUE1_HINTA_KM
        else:
            cost += NUPPI_ALUE1_YLARAJA * NUPPI_ALUE1_HINTA_KM
            distance -= NUPPI_ALUE1_YLARAJA

            if distance < (NUPPI_ALUE2_YLARAJA - NUPPI_ALUE1_YLARAJA):
                cost += distance * NUPPI_ALUE2_HINTA_KM
            else:
                cost += (NUPPI_ALUE2_YLARAJA - NUPPI_ALUE1_YLARAJA) * NUPPI_ALUE2_HINTA_KM
                distance -= (NUPPI_ALUE2_YLARAJA - NUPPI_ALUE1_YLARAJA)

                cost += distance * NUPPI_ALUE3_HINTA_KM
        return cost

    def laske_kasetti(self, distance):
        cost = KASETTI_LAHTOHINTA_KUORMA
        if distance < KASETTI_ALUE1_YLARAJA:
            cost += distance * KASETTI_ALUE1_HINTA_KM
        else:
            cost += KASETTI_ALUE1_YLARAJA * KASETTI_ALUE1_HINTA_KM
            distance -= KASETTI_ALUE1_YLARAJA

            if distance < (KASETTI_ALUE2_YLARAJA - KASETTI_ALUE1_YLARAJA):
                cost += distance * KASETTI_ALUE2_HINTA_KM
            else:
                cost += (KASETTI_ALUE2_YLARAJA - KASETTI_ALUE1_YLARAJA) * KASETTI_ALUE2_HINTA_KM
                distance -= (KASETTI_ALUE2_YLARAJA - KASETTI_ALUE1_YLARAJA)

                cost += distance * KASETTI_ALUE3_HINTA_KM
        return cost

    def get_total(self):
        total = 0

        for item, quantity in self.items:
            cost = 0

            if item.subtype == 'kuorikate':
                cost = HINTA_KUORIKATE_KIINTEA
            else:
                distance = find_closest(item.locations, self.destination)['distance']
                print("dist: " + str(distance))
                if item.maara_per_kpl * quantity < NUPPI_MAX_PAINO:
                    cost = self.laske_nuppi(distance)
                else:
                    while quantity > 0:
                        cost = self.laske_kasetti(distance)
                        quantity -= KASETTI_MAX_PAINO / item.maara_per_kpl
            total += cost
        return total
