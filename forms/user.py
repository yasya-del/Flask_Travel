from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, FieldList
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Логин/Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия')
    name = StringField('Имя', validators=[DataRequired()])
    age = StringField('Возраст')
    submit = SubmitField('Зарегистрироваться')


class ProfileForm(FlaskForm):
    email = EmailField('Логин/Email', validators=[DataRequired()])
    surname = StringField('Фамилия')
    name = StringField('Имя', validators=[DataRequired()])
    age = StringField('Возраст')
    submit = SubmitField('Подтвердить изменения')


class LoginForm(FlaskForm):
    email = EmailField('Логин/Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddPhotoForm(FlaskForm):
    img = FileField('Выберите фото', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'webp',
                                                                              'tiff', 'svg'], 'ТОлько картинки!')])
    submit = SubmitField('Добавить')