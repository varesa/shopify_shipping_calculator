from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

from .config_manager import initialize_configs

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    # Check config files, stops application if invalid
    initialize_configs()

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
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
    config.scan()
    return config.make_wsgi_app()
