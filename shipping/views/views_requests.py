from pyramid.testing import DummyRequest
from pyramid.view import view_config

from ..models import (
    DBSession,
    QuoteRequest
)

from ..utils import prettify_json

from .views_callback import view_callback

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
