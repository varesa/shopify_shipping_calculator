#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.orm.session import make_transient

from shipping.models import DBSession, ShippingLocation, Product


@view_config(route_name='data_products', renderer='../../templates/data_products.pt')
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

        DBSession.query(Product).delete()

        for line in products_csv:
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    line = line.decode('ISO-8859-1')
                except:
                    return Response('<html><body>Invalid encoding</body></html>')
            parts = line.split(';')
            if len(parts) < 5:
                 continue
            handle = parts[0].strip()
            type = parts[1].strip()
            subtype = parts[2].strip()
            maara_per_kpl = parts[3].strip()
            locations = []
            for field in parts[4:]:
                location = DBSession.query(ShippingLocation).filter_by(name=field.strip()).first()
                if location:
                    locations.append(location)
            print(locations)
            DBSession.add(Product(handle=handle, type=type, subtype=subtype, maara_per_kpl=maara_per_kpl, locations=locations))
            if handle == "testi-Test2":
                pass # assert False

    products = DBSession.query(Product).all()

    return {'products': products}


@view_config(route_name='export_products')
def view_export_products(request):
    contents = ""
    for product in DBSession.query(Product).all():
        contents += product.handle + ';' + product.type + ';' + product.subtype + ';' + str(product.maara_per_kpl)
        for location in product.locations:
            contents += ';' + str(location.name)
        contents += '\n'
#            ';'.join(product.locations) + '\n'

    resp = Response()
    resp.charset = "utf-8"
    resp.text = contents
    resp.headerlist.append(("Content-Disposition", "attachment"))
    return resp
