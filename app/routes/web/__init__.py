from flask import Blueprint
from app.routes.web import auth, main
from app.routes.web.event_route import events_bp


bp = Blueprint('web', __name__)
