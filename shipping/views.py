from pyramid.response import Response
from pyramid.view import view_config

from datetime import datetime
import json

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    QuoteRequest
    )

from .api_auth import create_session

from shopify import CarrierService

@view_config(route_name='home', renderer='templates/main.pt')
def my_view(request):
    return {'one': "abc", 'project': 'shipping'}

@view_config(route_name='callback')
def view_callback(request):
    q = QuoteRequest()
    q.date = datetime.now()
    q.json = request.body
    DBSession.add(q)

    return Response('')

@view_config(route_name='setup', renderer='templates/setup.pt')
def view_setup(request):
    create_session()
    services = CarrierService.find()
    return {'services': services}

@view_config(route_name='setup_addservice', renderer='templates/generic_text.pt')
def view_setup_addservice(request):
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
    requests = DBSession.query(QuoteRequest).all()
    return {'requests': requests}


def prettify_json(data):
    expanded = json.loads(data)
    return json.dumps(expanded, indent=4, separators=(',', ': '))


@view_config(route_name='request_details', renderer='templates/request_details.pt')
def view_request_details(request):
    id = request.matchdict['id']
    req = DBSession.query(QuoteRequest).filter_by(id=id).first()
    req.json = prettify_json(req.json)
    return {'request': req}