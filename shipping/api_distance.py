from urllib.parse import quote_plus
from urllib.request import urlopen

import json

from math import ceil

from .exceptions import InvalidLocationException

baseurl = "http://maps.googleapis.com/maps/api/distancematrix/json?"


def url_from_json(location_json):
    """
    Encode a location represented by a dictionary of values into a
    string that can be passed as a GMaps parameter
    :param location_json: Dictionary that represents a location
    :type location_json: str
    :return: An url-encoded (with plus-signs) string representing the location
    :rtype: str
    """
    location = json.loads(location_json)
    full_address = ""
    full_address += location['address1'] + ", "
    full_address += (location['address2'] + ", ") if len(location['address2']) > 0 else ''
    full_address += location['postal_code'] + " "
    full_address += location['city'] + ", "
    full_address += location['country']

    return quote_plus(full_address)


def url_from_string(location_string):
    """
    Encode a location represented by a string into a url-form that can be passed to GMaps
    :param location_string: String to be URL-encoded
    :type location_string: str
    :return: An URL-encoded (with plus-signs) string representing the location
    :rtype: str
    """
    return quote_plus(location_string)


def get_distance_url_url(origin_url, destination_url):
    """
    Do a request to GMaps for a distance between two points
    :param origin_url: First of the two points in JSON
    :type origin_url: str
    :param destination_url: Second of the two points in JSON
    :type destination_url: str
    :return: distance between locations in kilometers, rounded up
    :rtype: int
    """

    print("Requesting distance")

    request_url = baseurl + "origins=" + origin_url + "&destinations=" + destination_url
    response_json = urlopen(request_url).read().decode('utf-8')
    response = json.loads(response_json)

    print("Distance received")

    if response['rows'][0]['elements'][0]['status'] != 'OK':
        raise InvalidLocationException

    return ceil(int(response['rows'][0]['elements'][0]['distance']['value'])/1000.0)


def get_distance_json_json(origin_json, destination_json):
    """
    Get the distance between two points that are both represented in JSON
    :param origin_json: JSON-string for the origin point
    :type origin_json: str
    :param destination_json: JSON-string for the destination point
    :type destination_json: str
    :return: distance as returned by :method: get_distance_url_url
    """
    get_distance_url_url(url_from_json(origin_json), url_from_json(destination_json))


def get_distance_string_json(origin_string, destination_json):
    """
    Get the distance between two points where origin is in string form and destination in JSON
    :param origin_string: string for the origin point
    :type origin_string: str
    :param destination_json: JSON-string for the destination point
    :type destination_json: str
    :return: distance as returned by :method: get_distance_url_url
    """
    get_distance_url_url(url_from_string(origin_string), url_from_json(destination_json))


def shortest_distance_string_json(origin_strings, destination_json):
    """
    Find the shortest pair from a group of origins and a destination
    :param origin_strings: Array of origins
    :type origin_strings: array of strings
    :param destination_json: destination in JSON form
    :type destination_json: str
    :return: Distance between the closest two points
    """
    min_dist = None

    for origin in origin_strings:
        dist = get_distance_string_json(origin, destination_json)
        if min_dist == None or dist < min_dist:
            min_dist = dist

    return min_dist