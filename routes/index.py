from flask import render_template
from . import routes

@routes.route("/", defaults={'path': 'index.html'})
def index(path):
    return render_template(path)