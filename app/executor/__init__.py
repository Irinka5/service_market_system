from flask import Blueprint

executor = Blueprint('executor', __name__)

from . import routes
