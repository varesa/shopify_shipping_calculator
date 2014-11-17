class CategoryMuut:

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
        pass