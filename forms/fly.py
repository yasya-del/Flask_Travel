from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, FieldList, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError
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
    start_date = DateField('Когда', validators=[DataRequired()])
    end_date = DateField('Обратно')
    adult = StringField('Кол-во взрослых(12 лет и старше)', validators=[DataRequired()])
    child = StringField('Кол-во детей(от 2 до 11 лет)')
    baby = StringField('Кол-во младенцев(до 2 лет, без места)')
    clas = SelectField('Класс обслуживания', choices=classes, validators=[DataRequired()])
    submit = SubmitField('Искать билеты')


