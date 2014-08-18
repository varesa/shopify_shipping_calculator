from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .routes import configure_routes

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

    configure_routes(config)

    config.scan()

    return config.make_wsgi_app()
