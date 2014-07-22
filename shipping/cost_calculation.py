import json

test_origin = "Villähde, Finland"

def calculate_shipping(requestjson):
    data = json.loads(requestjson)
    items = data['rates']['items']
    destination = data['rates']['destination']

    for item in items:
        print(item)
