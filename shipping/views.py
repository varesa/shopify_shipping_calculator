from pyramid.response import Response
from pyramid.testing import DummyRequest
from pyramid.view import view_config

from datetime import datetime
import json

from .models import (
    DBSession,
    QuoteRequest
)

from shopify import CarrierService
from .api_auth import create_session

from .cost_calculation import calculate_shipping

from .utils import prettify_json


@view_config(route_name='home', renderer='templates/main.pt')
def view_main(request):
    """
    View method for the navigational frontpage
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values to be used in the template
    """
    return {}


@view_config(route_name='callback')
def view_callback(request, save=True):
    """
    View method for the shopify rates callback
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values to be used in the template
    """
    if save:
        q = QuoteRequest()
        q.date = datetime.now()
        q.json = request.body
        DBSession.add(q)

    calculate_shipping(request.body.decode('utf-8'))

    responsedata = json.dumps(
        {
            'rates': [
                {
                    "service_name": 'TestShipping',
                    "service_code": 'tst',
                    "total_price":  '15000',
                    "currency": "EUR",
                    "min_delivery_date": "2013-10-25 14:48:45 +0200",
                    "max_delivery_date": "2013-10-25 14:48:45 +0200"
                }
            ]
        }
    )

    return Response(responsedata)


@view_config(route_name='setup', renderer='templates/setup.pt')
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


@view_config(route_name='setup_addservice', renderer='templates/generic_text.pt')
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


@view_config(route_name='requests', renderer='templates/requests.pt')
def view_requests(request):
    """
    View method for viewing the saved requests from shopify
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values to be used in the template
    """
    requests = DBSession.query(QuoteRequest).all()
    return {'requests': requests}


@view_config(route_name='request_details', renderer='templates/request_details.pt')
def view_request_details(request):
    """
    View method for viewing the detailed data contained in a saved request
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values to be used in the template
    """
    id = request.matchdict['id']
    req = DBSession.query(QuoteRequest).filter_by(uuid=id).first()
    req.json = prettify_json(req.json)
    return {'request': req}


@view_config(route_name='request_test', renderer='templates/request_test.pt')
def view_request_test(request):
    """
    View method to test the calculation using a saved request. Calls view_callback
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values to be used in the template
    """
    id = request.matchdict['id']
    req = DBSession.query(QuoteRequest).filter_by(uuid=id).first()

    fakereq = DummyRequest()
    fakereq.body = req.json.encode('utf-8')
    response = view_callback(fakereq, save=False)
    response_data = response.body.decode('utf-8')

    response_data = prettify_json(response_data)

    return {'result': response_data}
