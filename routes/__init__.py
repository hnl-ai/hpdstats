from flask import Blueprint
routes = Blueprint('routes', __name__)

from .index import *
from .table import *
from .map import *
from .archive import *
