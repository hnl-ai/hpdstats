# -*- coding: utf-8 -*-
"""The index module."""
from flask import Blueprint, render_template

routes = Blueprint('routes', __name__)

@routes.route("/", defaults={'path': 'index.html'})
def index_route(path):
    """The index route."""
    return render_template(path)

@routes.route("/activedispatches", defaults={'path': 'activedispatches.html'})
def activedispatches_route(path):
    """The active dispatches route."""
    return render_template(path)

@routes.route("/archive", defaults={'path': 'archive.html'})
def archive_route(path):
    """The archive route."""
    return render_template(path)

@routes.route("/map", defaults={'path': 'map.html'})
def map_route(path):
    """The map route."""
    return render_template(path)

@routes.route("/table", defaults={'path': 'table.html'})
def table_route(path):
    """The table route."""
    return render_template(path)
