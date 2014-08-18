from pyramid.view import view_config
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


@view_config(route_name='data_lastauspaikat', renderer='../templates/data_lastauspaikat.pt')
def view_data_lastauspaikat(request):
    """
    View method for listing data associated with different loading locations
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values for template rendering
    """

    locations = DBSession.query(ShippingLocation).all()

    return {'locations': locations}


@view_config(route_name='data_tuotteet', renderer='../templates/data_tuotteet.pt')
def view_data_tuotteet(request):
    """
    View method for listing data associated with different products
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values for template rendering
    """
    return {}