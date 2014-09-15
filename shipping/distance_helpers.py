from .api_distance import get_distance_string_json
from .models import ShippingLocation
from .exceptions import InvalidLocationException


def find_closest(locations, destination_json):
    """
    Find the shortest pair from a group of origins and a destination
    :param origin_strings: Array of locations
    :param destination_json: destination in JSON form
    :type destination_json: str
    :return: Dict with 'location' and 'distance'
    :rtype: dict
    """
    min_dist = None
    closest = None

    for location in locations:
        try:
            dist = get_distance_string_json(location.address, destination_json)
        except InvalidLocationException:
            print("[ERROR] INVALID LOCATION DATA") # TODO: Add real logging/error reporting
            continue

        if not min_dist or dist < min_dist:
            min_dist = dist
            closest = location

    if closest is None:
        raise InvalidLocationException

    return {'location': closest, 'distance': min_dist}