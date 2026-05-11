from flask import render_template, redirect, url_for, flash, Blueprint, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db
from app.forms.event_form import EventForm
from app.models.event_model import Event, ExpenseCategory, EventExpense

events_bp = Blueprint('events', __name__, url_prefix='/events')

UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@events_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if not current_user.is_admin():
        flash('Доступ запрещен. Только для администраторов', 'danger')
        return redirect(url_for('main.index'))

    form = EventForm()

    if form.validate_on_submit():
        event = Event(
            name=form.name.data,
            event_date=form.event_date.data,
            start_time=form.start_time.data,
            duration_hours=form.duration_hours.data,
            description=form.description.data,
            activity_type=form.activity_type.data,
            is_published=form.is_published.data,
            created_by=current_user.id,
            planned_participants=form.planned_participants.data,
            planned_organizers=form.planned_organizers.data,
            planned_experts=form.planned_experts.data,
            planned_guests=form.planned_guests.data,
            discount_cards_count=form.discount_cards_count.data,
            discount_amount=form.discount_amount.data,
            participation_cost=form.participation_cost.data
        )

        db.session.add(event)
        db.session.flush()

        expenses_data = request.form.get('expenses_data')
        if expenses_data:
            import json
            expenses_dict = json.loads(expenses_data)
            for category_id, amount in expenses_dict.items():
                if amount and float(amount) > 0:
                    event_expense = EventExpense(
                        event_id=event.id,
                        category_id=int(category_id),
                        amount=float(amount)
                    )
                    db.session.add(event_expense)

        event.calculate_financials()

        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join('uploads', filename)
            form.image.data.save(os.path.join('app/static', image_path))
            event.image_path = image_path

        db.session.commit()
        flash('Мероприятие создано', 'success')
        return redirect(url_for('main.index'))

    categories = ExpenseCategory.query.order_by(ExpenseCategory.order).all()
    categories_json = [{'id': c.id, 'name': c.name, 'is_default': c.is_default} for c in categories]

    return render_template('events/event_form.html', form=form, categories=categories_json, event=None,
                           title='Создание мероприятия')


@events_bp.route('/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    if not current_user.is_admin():
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('main.index'))

    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)

    categories = ExpenseCategory.query.order_by(ExpenseCategory.order).all()
    categories_json = [{'id': c.id, 'name': c.name, 'is_default': c.is_default} for c in categories]

    existing_expenses = {e.category_id: e.amount for e in event.expenses_list}

    if form.validate_on_submit():
        event.name = form.name.data
        event.event_date = form.event_date.data
        event.start_time = form.start_time.data
        event.duration_hours = form.duration_hours.data
        event.description = form.description.data
        event.activity_type = form.activity_type.data
        event.is_published = form.is_published.data
        event.planned_participants = form.planned_participants.data
        event.planned_organizers = form.planned_organizers.data
        event.planned_experts = form.planned_experts.data
        event.planned_guests = form.planned_guests.data
        event.discount_cards_count = form.discount_cards_count.data
        event.discount_amount = form.discount_amount.data
        event.participation_cost = form.participation_cost.data

        EventExpense.query.filter_by(event_id=event.id).delete()

        expenses_data = request.form.get('expenses_data')
        if expenses_data:
            import json
            expenses_dict = json.loads(expenses_data)
            for category_id, amount in expenses_dict.items():
                if amount and float(amount) > 0:
                    event_expense = EventExpense(
                        event_id=event.id,
                        category_id=int(category_id),
                        amount=float(amount)
                    )
                    db.session.add(event_expense)

        event.calculate_financials()

        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join('uploads', filename)
            form.image.data.save(os.path.join('app/static', image_path))
            event.image_path = image_path

        db.session.commit()
        flash('Мероприятие обновлено', 'success')
        return redirect(url_for('main.event_detail', event_id=event.id))

    return render_template('events/event_form.html', form=form, categories=categories_json, event=event,
                           existing_expenses=existing_expenses, title='Редактирование мероприятия')


@events_bp.route('/delete/<int:event_id>')
@login_required
def delete_event(event_id):
    if not current_user.is_admin():
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('main.index'))

    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Мероприятие удалено', 'success')
    return redirect(url_for('main.index'))


@events_bp.route('/categories/add', methods=['POST'])
@login_required
def add_category():
    if not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403

    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Name required'}), 400

    max_order = db.session.query(db.func.max(ExpenseCategory.order)).scalar() or 0
    category = ExpenseCategory(name=name, is_default=False, order=max_order + 1)
    db.session.add(category)
    db.session.commit()

    return jsonify({'id': category.id, 'name': category.name, 'is_default': category.is_default})


@events_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403

    category = ExpenseCategory.query.get_or_404(category_id)
    if category.is_default:
        return jsonify({'error': 'Cannot delete default category'}), 400

    db.session.delete(category)
    db.session.commit()

    return jsonify({'success': True})
