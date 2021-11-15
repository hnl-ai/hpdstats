from flask import render_template
from . import routes

@routes.route("/archive", defaults={'path': 'archive.html'})
def archive(path):
    return render_template(path)