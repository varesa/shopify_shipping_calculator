#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


from pyramid.view import view_config
from pyramid.response import Response

from shipping.models import DBSession, ShippingLocation


@view_config(route_name='data_locations', renderer='../../templates/data_locations.pt')
def view_data_locations(request):
    """
    View method for listing data associated with different loading locations
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values for template rendering
    """

    if 'file_locations' in request.POST.keys():
        locations_csv = request.POST['file_locations'].file.readlines()

        locations = []

        for line in locations_csv:
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    line = line.decode('ISO-8859-1')
                except:
                    return Response('<html><body>Invalid encoding</body></html>')

            parts = line.split(';')
            name = parts[0].strip()
            address = parts[1].strip()

            locations.append((name, address))

        if len(locations) > 0:
            # We have somewhat valid data
            DBSession.query(ShippingLocation).delete()

        for location in locations:
            DBSession.add(ShippingLocation(name=location[0], address=location[1]))

    locations = DBSession.query(ShippingLocation).all()

    return {'locations': locations}


@view_config(route_name='export_locations')
def view_export_locations(request):
    contents = ""
    for location in DBSession.query(ShippingLocation).all():
        contents += location.name + ';' + location.address + '\n'

    resp = Response()
    resp.charset = "utf-8"
    resp.text = contents
    resp.headerlist.append(("Content-Disposition", "attachment"))
    return resp