from flask import render_template
from . import routes

@routes.route("/table", defaults={'path': 'table.html'})
def table(path):
    return render_template(path)
