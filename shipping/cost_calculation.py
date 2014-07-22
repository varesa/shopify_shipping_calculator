import json


def calculate_shipping(json):
    data = json.loads(json)
    items = data['rates']['items']
    destination = data['rates']['destination']
