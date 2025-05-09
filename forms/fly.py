from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, FieldList, SelectField
from wtforms.validators import DataRequired
import sqlite3


class FlyForm(FlaskForm):
    con = sqlite3.connect('db/travel.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT city FROM airports""").fetchall()
    con.close()
    cities = [x[0] for x in result]
    classes = ['Эконом', 'Комфорт', 'Бизнес', 'Первый класс']
    start = SelectField('Откуда', choices=cities, validators=[DataRequired()])
    finish = SelectField('Куда', choices=cities, validators=[DataRequired()])
    start_date = StringField('Когда', validators=[DataRequired()])
    end_date = StringField('Обратно')
    adult = StringField('Взрослые(12 лет и старше)', validators=[DataRequired()])
    child = StringField('Дети(от 2 до 11 лет)', validators=[DataRequired()])
    baby = StringField('Младенцы(до 2 лет, без места)', validators=[DataRequired()])
    clas = SelectField('Класс обслуживания', choices=classes, validators=[DataRequired()])
    submit = SubmitField('Искать билеты')