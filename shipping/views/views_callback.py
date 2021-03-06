#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


import json
import traceback
from datetime import datetime

from pyramid.view import view_config
from pyramid.response import Response
import transaction

from ..models import DBSession
from ..models import QuoteRequest
from ..shipping_logic.cost_calculation import calculate_shipping


@view_config(route_name='callback')
def view_callback(request, save=True):
    """
    View method for the shopify rates callback
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values to be used in the template
    """
    if save:
        with transaction.manager:
            q = QuoteRequest()
            q.date = datetime.now()
            q.json = request.body
            DBSession.add(q)

    if save:
        try:
            shipping = calculate_shipping(request.body.decode('utf-8'))
        except:
            traceback.print_exc()
    else:
        shipping = calculate_shipping(request.body.decode('utf-8'))

    responsedata = json.dumps(
        {
            'rates': [
                {
                    "service_name": 'TestShipping',
                    "service_code": 'tst',
                    "total_price":  shipping,
                    "currency": "EUR",
                    "min_delivery_date": "2013-10-25 14:48:45 +0200",
                    "max_delivery_date": "2013-10-25 14:48:45 +0200"
                }
            ]
        }
    )

    return Response(responsedata)