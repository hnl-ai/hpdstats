# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from flask_caching import Cache

from .routes import routes
from .routes.api import create_archives_route, create_records_route

def create_app():
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.
    """
    app = Flask(__name__, static_url_path='/static')
    app.url_map.strict_slashes = False
    cache = register_cache(app)
    register_blueprints(app)
    register_routes(app, cache)
    return app

def register_cache(app):
    """Register Flask cache."""
    cache = Cache(config={'CACHE_TYPE': 'simple'})
    cache.init_app(app)
    return cache

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(routes)

def register_routes(app, cache):
    """Register Flask routes."""
    create_records_route(app, cache)
    create_archives_route(app, cache)
