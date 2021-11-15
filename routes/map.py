from flask import render_template
from . import routes

@routes.route("/map", defaults={'path': 'map.html'})
def map(path):
    return render_template(path)
