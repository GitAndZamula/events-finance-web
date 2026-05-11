from app import db
from app.models.event_model import ExpenseCategory


def init_expense_categories():
    default_categories = [
        'Аренда помещения',
        'Залог в кафе',
        'Оплата эксперта',
        'Стоимость материалов',
        'Стоимость инструментов',
        'Оплата питания',
        'Оплата напитков',
        'Заработная плата',
        'Транспортные расходы',
        'Прочие расходы'
    ]

    for i, category in enumerate(default_categories):
        exists = ExpenseCategory.query.filter_by(name=category).first()
        if not exists:
            new_category = ExpenseCategory(name=category, is_default=True, order=i)
            db.session.add(new_category)

    db.session.commit()
