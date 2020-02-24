from flask import Blueprint

main = Blueprint('main', __name__)

from soundstream.routes import routes, events
