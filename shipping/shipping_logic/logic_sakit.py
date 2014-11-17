from ..models import Product

from ..distance_helpers import find_closest


class CategorySakit:

    destination = None
    ":type: str (json)"
    items = []
    ":type: (Product, int)"

    def __init__(self, destination):
        self.destination = destination

    def add_item(self, item, quantity):
        self.items.append((item, quantity))

    def has_items(self):
        return len(self.items) > 0

    def sort_by_origin(self, items):
        bag_locations = []
        for item, quantity in items:
            closest = find_closest(item.locations, self.destination)

            found = False
            for bag_location in bag_locations:
                if bag_location['location'] == closest['location']:
                    found = True
                    bag_location['bags'] += quantity

            if not found:
                bag_locations.append({'location': closest['location'],
                                      'distance': closest['distance'],
                                      'bags': quantity})

    def get_total(self):
        bag_locations = self.sort_by_origin(self.items)

        return 0

"""found = False
    for bag_location in bag_locations:
        if bag_location['location'] == closest['location']:
            found = True
            bag_location['bags'] += item['quantity']

    if not found:
        bag_locations.append({'location': closest['location'], 'distance': closest['distance'], 'bags': item['quantity']})"""

"""for bag_location in bag_locations:
        print(str(bag_location['distance']) + " km * " + str(bag_location['bags']) + " bags = " +
              str(bags_price_per_km * bag_location['distance'] * ceil(bag_location['bags']/18)))
        total_price += bags_price_per_km * bag_location['distance'] * ceil(bag_location['bags']/18)"""