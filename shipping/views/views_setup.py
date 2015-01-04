#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


from pyramid.view import  view_config

from shopify import CarrierService

from ..api_auth import create_session


@view_config(route_name='setup', renderer='../templates/setup.pt')
def view_setup(request):
    """
    View method for the setup page, shows registered CarrierServices
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values to be used in the template
    """
    create_session()
    services = CarrierService.find()
    return {'services': services}


@view_config(route_name='setup_addservice', renderer='../templates/generic_text.pt')
def view_setup_addservice(request):
    """
    View method for a page for registering a new CarrierService
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values to be used in the template
    """
    create_session()

    c = CarrierService()
    c.name = "Test"
    c.callback_url = "http://finbit.dy.fi:6545/callback"
    c.format = "json"
    c.service_discovery = True
    c.save()

    return {'header': "Service added", 'text': "<a href='/'>Return</a>"}
