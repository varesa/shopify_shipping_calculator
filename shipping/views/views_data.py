from pyramid.view import view_config
from pyramid.response import Response

from ..models import DBSession, ShippingLocation, Product


@view_config(route_name='data', renderer='../templates/data.pt')
def view_data(request):
    """
    View method for listing different data-types used by the application
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values for template rendering
    """
    return {}


@view_config(route_name='data_locations', renderer='../templates/data_locations.pt')
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


@view_config(route_name='data_products', renderer='../templates/data_products.pt')
def view_data_products(request):
    """
    View method for listing data associated with different products
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values for template rendering
    """

    if 'file_products' in request.POST.keys():
        products_csv = request.POST['file_products'].file.readlines()

        products = []

        for line in products_csv:
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    line = line.decode('ISO-8859-1')
                except:
                    return Response('<html><body>Invalid encoding</body></html>')

            parts = line.split(';')
            handle = parts[0].strip()
            type = parts[1].strip()
            subtype = parts[2].strip()
            locations = []
            for field in parts[3:]:
                location = DBSession.query(ShippingLocation).filter_by(name=field.strip()).first()
                if location:
                    locations.append(location)

            products.append((handle, type, locations))

        if len(products) > 0:
            # We have somewhat valid data
            DBSession.query(Product).delete()

        for product in products:
            DBSession.add(Product(handle=product[0], type=product[1], locations=product[2]))

    products = DBSession.query(Product).all()

    return {'products': products}