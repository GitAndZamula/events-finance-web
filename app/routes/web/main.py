from flask import render_template, Blueprint
from app.models.event_model import Event

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    events = Event.query.filter_by(is_published=True).order_by(Event.event_date.desc()).all()
    return render_template('index.html', events=events)

@bp.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('events/detail.html', event=event)
