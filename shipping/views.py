from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    )

from .api_auth import create_session

from shopify import CarrierService

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'one': "abc", 'project': 'shipping'}

@view_config(route_name='setup', renderer='templates/setup.pt')
def view_setup(request):
    create_session()

    services = CarrierService.find()
    print(services)
    return {}

@view_config(route_name='setup-addservice', renderer='templates/generic_text.pt')
def view_setup_addservice(request):
    return {'text': "Service added."}


