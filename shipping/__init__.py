#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .routes import configure_routes

from .models import (
    DBSession,
    Base,
    )

from .config_manager import initialize_configs

def pdb_wrapper(app):
    def pdb_app(environ, start_response):
        #import pdb; pdb.set_trace()
        print(environ['PATH_INFO'])
        return app(environ, start_response)
    return pdb_app

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    # Check config files, stops application if invalid
    initialize_configs()

    engine = engine_from_config(settings, 'sqlalchemy.', pool_recycle=3600)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    config.include('pyramid_chameleon')

    configure_routes(config)

    config.scan()

    return pdb_wrapper(config.make_wsgi_app())
