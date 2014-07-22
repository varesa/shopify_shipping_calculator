from urllib.parse import quote_plus
from urllib.request import urlopen

import json

from math import ceil

baseurl = "http://maps.googleapis.com/maps/api/distancematrix/json?"


def url_from_dict(location):
    full_address = ""
    full_address += location['address1'] + ", "
    full_address += (location['address2'] + ", ") if len(location['address2']) > 0 else ''
    full_address += location['zip'] + " "
    full_address += location['city'] + ", "
    full_address += location['country']

    return quote_plus(full_address)


def get_distance(origin, destination):
    origin_url = url_from_dict(origin)
    dest_url = url_from_dict(destination)

    request_url = baseurl + "origins=" + origin_url + "&destinations=" + dest_url
    response_json = urlopen(request_url).read().decode('utf-8')
    response = json.loads(response_json)

    return ceil(int(response['rows']['elements']['distance']['value'])/1000.0)