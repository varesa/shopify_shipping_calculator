import json

test_origin = "Villähde, Finland"

def calculate_shipping(json):
    data = json.loads(json)
    items = data['rates']['items']
    destination = data['rates']['destination']

    for item in items:
        print(item)
