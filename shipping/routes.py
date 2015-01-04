#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


def configure_routes(config):
    """
    Add routes to the pyramid config
    :param config: pyramid config to add routes to
    :type config: pyramid.config.Configurator
    :return: None
    """

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    # Shopify callback for requesting rates
    config.add_route('callback', '/callback')

    # Links from shopify
    config.add_route('preferences', '/preferences')
    config.add_route('admin', '/admin')
    config.add_route('proxy', '/proxy')

    # Managing product and location data
    config.add_route('data', '/data')
    config.add_route('data_locations', '/data/locations')
    config.add_route('data_products', '/data/products')
    config.add_route('export_locations', '/export/locations.csv')
    config.add_route('export_products', '/export/products.csv')

    # Listing past requests from shopify
    config.add_route('requests', '/requests')
    config.add_route('request_details', '/requests/{id}')
    config.add_route('request_test', '/requests/{id}/test')

    # Registering with shopify
    config.add_route('setup', '/setup')
    config.add_route('setup_addservice', "/setup/addservice")