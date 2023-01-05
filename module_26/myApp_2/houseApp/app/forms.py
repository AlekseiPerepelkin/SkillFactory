from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,HiddenField
from wtforms.validators import DataRequired

class EditForm(FlaskForm):
    id = HiddenField("flatId")
    title = StringField('Заголовок объявления')
    city = StringField('Город')
    rooms = IntegerField('Количество комнат')
    area = StringField('Площадь')
    floor = IntegerField('Этаж')
    cost = IntegerField('Стоимость')
    submit = SubmitField('Сохранить')
    predict = SubmitField('Предсказать')
