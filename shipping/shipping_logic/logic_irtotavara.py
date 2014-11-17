from ..distance_helpers import find_closest
from ..models import Product


HINTA_KUORIKATE_KIINTEA = 50

NUPPI_MAX_PAINO = 18.0
NUPPI_LAHTOHINTA_KUORMA = 58.0

NUPPI_ALUE1_YLARAJA = 7.0
NUPPI_ALUE1_HINTA_KM = 0.0

NUPPI_ALUE2_YLARAJA = 40.0
NUPPI_ALUE2_HINTA_KM = 5.0

NUPPI_ALUE3_YLARAJA = None
NUPPI_ALUE3_HINTA_KM = 4.4



KASETTI_MAX_PAINO = 38.0
KASETTI_LAHTOHINTA_KUORMA = 128.0

KASETTI_ALUE1_YLARAJA = 10
KASETTI_ALUE1_HINTA_KM = 0.0

KASETTI_ALUE2_YLARAJA = 90.0
KASETTI_ALUE2_HINTA_KM = 4.2

KASETTI_ALUE3_YLARAJA = None
KASETTI_ALUE3_HINTA_KM = 3.8


class CategoryIrtotavara():

    destination = None
    ":type: str"
    items = []
    ":type: list of (Product, int)"

    def __init__(self, destination):
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
                if item.maara_per_yksikko * quantity < NUPPI_MAX_PAINO:
                    cost = self.laske_nuppi(distance)
                else:
                    while quantity > 0:
                        cost = self.laske_kasetti(distance)
                        quantity -= KASETTI_MAX_PAINO / item.maara_per_yksikko

            total += cost

"""irtokuormat.append({'location': closest['location'], 'distance': closest['distance'], 'amount': item['quantity']})"""

"""

    for irtokuorma in irtokuormat:
        print(str(irtokuorma['distance']) + " km * " + str(irtokuorma['amount']) + " tn = " +
              str(irtokuorma_hinta(irtokuorma['distance'], irtokuorma['amount'])))
        total_price += irtokuorma_hinta(irtokuorma['distance'], irtokuorma['amount'])"""