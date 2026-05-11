from app import create_app, db
from app.models.user import User
from app.models.event_model import Event, ExpenseCategory, EventExpense
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    default_categories = [
        'Аренда помещения', 'Залог в кафе', 'Оплата эксперта',
        'Стоимость материалов', 'Стоимость инструментов', 'Оплата питания',
        'Оплата напитков', 'Заработная плата', 'Транспортные расходы', 'Прочие расходы'
    ]

    for i, category in enumerate(default_categories):
        exists = ExpenseCategory.query.filter_by(name=category).first()
        if not exists:
            new_category = ExpenseCategory(name=category, is_default=True, order=i)
            db.session.add(new_category)

    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)

    db.session.commit()
    print("Database initialized successfully!")
