def configure_routes(config):
    """
    Add routes to the pyramid config
    :param config: pyramid config to add routes to
    :type config: pyramid.config.Configurator
    :return: None
    """

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('callback', '/callback')

    config.add_route('preferences', '/preferences')
    config.add_route('admin', '/admin')
    config.add_route('proxy', '/proxy')

    config.add_route('setup', '/setup')
    config.add_route('setup_addservice', "/setup/addservice")

    config.add_route('requests', '/requests')
    config.add_route('request_details', '/requests/{id}')
    config.add_route('request_test', '/requests/{id}/test')