#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


from pyramid.view import view_config


@view_config(route_name='data', renderer='../../templates/data.pt')
def view_data(request):
    """
    View method for listing different data-types used by the application
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values for template rendering
    """
    return {}

