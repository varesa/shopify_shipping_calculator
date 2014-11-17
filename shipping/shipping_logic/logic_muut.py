class CategoryMuut:

    destination = None
    items = []

    def __init__(self, destination):
        self.destination = destination

    def add_item(self, item, quantity):
        self.items.append((item, quantity))

    def has_items(self):
        return len(self.items) > 0

    def get_total(self):
        pass