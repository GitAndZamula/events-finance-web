from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, TimeField, FloatField, TextAreaField, SelectField, SubmitField, \
    BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class EventForm(FlaskForm):
    name = StringField('Название мероприятия', validators=[DataRequired(), Length(max=200)])
    event_date = DateField('Дата проведения', validators=[DataRequired()])
    start_time = TimeField('Время начала', validators=[DataRequired()])
    duration_hours = FloatField('Продолжительность (часы)', validators=[DataRequired(), NumberRange(min=0.5, max=24)])
    activity_type = SelectField('Тип активности', choices=[
        ('Мастер-класс', 'Мастер-класс'), ('Лекция', 'Лекция'), ('Воркшоп', 'Воркшоп'),
        ('Семинар', 'Семинар'), ('Тренинг', 'Тренинг'), ('Другое', 'Другое')
    ], validators=[DataRequired()])
    description = TextAreaField('Описание')
    image = FileField('Изображение', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    is_published = BooleanField('Опубликовать')

    planned_participants = IntegerField('Обычные участники', default=0)
    planned_organizers = IntegerField('Организаторы', default=2)
    planned_experts = IntegerField('Эксперты', default=1)
    planned_guests = IntegerField('Приглашенные гости', default=0)
    discount_cards_count = IntegerField('Скидочные карты', default=0)
    discount_amount = FloatField('Скидка (%)', default=0)

    participation_cost = FloatField('Стоимость участия', default=0)

    submit = SubmitField('Сохранить')
