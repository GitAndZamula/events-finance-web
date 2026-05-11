from app import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    duration_hours = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    activity_type = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(500))
    is_published = db.Column(db.Boolean, default=True)

    planned_participants = db.Column(db.Integer, default=0)
    planned_organizers = db.Column(db.Integer, default=2)
    planned_experts = db.Column(db.Integer, default=1)
    planned_guests = db.Column(db.Integer, default=0)
    discount_cards_count = db.Column(db.Integer, default=0)
    discount_amount = db.Column(db.Float, default=0)

    total_expenses = db.Column(db.Float, default=0)
    self_cost = db.Column(db.Float, default=0)
    participation_cost = db.Column(db.Float, default=0)
    profit = db.Column(db.Float, default=0)

    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    creator = db.relationship('User', backref='events')

    def get_expenses(self):
        expenses = EventExpense.query.filter_by(event_id=self.id).all()
        return {e.category.name: e.amount for e in expenses}

    def calculate_financials(self):
        expenses = EventExpense.query.filter_by(event_id=self.id).all()
        total = sum(e.amount for e in expenses)
        self.total_expenses = total

        participants = self.planned_participants or 0
        discount_cards = self.discount_cards_count or 0
        paying = max(0, participants - discount_cards)

        if paying > 0:
            self.self_cost = total / paying
        else:
            self.self_cost = 0

        self.profit = (self.participation_cost * paying) - total

    def __repr__(self):
        return f'<Event {self.name}>'


class ExpenseCategory(db.Model):
    __tablename__ = 'expense_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<ExpenseCategory {self.name}>'


class EventExpense(db.Model):
    __tablename__ = 'event_expenses'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('expense_categories.id'), nullable=False)
    amount = db.Column(db.Float, default=0)

    event = db.relationship('Event', backref=db.backref('expenses_list', cascade='all, delete-orphan'))
    category = db.relationship('ExpenseCategory')
