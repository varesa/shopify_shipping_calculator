#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/main.pt')
def view_main(request):
    """
    View method for the navigational frontpage
    :param request: HTTP Request object
    :type request: pyramid.request.Request
    :return: Dictionary of values to be used in the template
    """
    return {}
