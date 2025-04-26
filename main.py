import datetime
from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.russian_cities import City
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import RegisterForm, LoginForm


app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def add_cities():
    cities = [['Москва', 'Москва — город федерального значения.', 'Культурный'],
              ['Санкт-Петербург', 'Санкт-Петербург — город федерального значения.', 'Культурный'],
              ['Казань', 'Республика Татарстан', 'Культурный'],
              ['Сочи', 'Краснодарский край', 'Рекреационный, активный'],
              ['Карелия', 'Республика Карелия', 'Активный'], ['Камчатка', 'Камчатский край', 'Активный'],
              ['Кисловодск', 'Ставропольский край', 'Рекреационный'], ['Кавказ', '-', 'Активный'],
              ['Крым', 'Республика Крым', 'Рекрационный'], ['Владивосток', 'Приморский край', 'Культурный'],
              ['Калининград', 'Калининградская область', 'Культурный'],
              ['Дербент', 'Республика Дагестан', 'Рекреационный']]
    db_sess = db_session.create_session()
    c = db_sess.query(City).all()
    print(c)
    for city in cities:
        city_bd = City(
            city=city[0],
            subject=city[1],
            tourism=city[2]
        )
        db_sess.add(city_bd)
    db_sess.commit()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Авторизация')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def title():
    return render_template('base.html',  title='Главная')


@app.route('/countries')
def choose_countries():
    return render_template('countries.html',  title='Страны')


@app.route('/country/<name>')
def country(name):
    return render_template(f'{name}.html', title=name)

@app.route('/country/map/<name>')
def open_map(name):
    from search import search_for_map
    search_for_map(name)
    return ''

@app.route('/my_profile')
def my_profile():
    if current_user.is_authenticated:
        return render_template(f'profile.html', title='Мой профиль')
    return redirect("/login")

@app.route('/my_plans')
def my_plans():
    if current_user.is_authenticated:
        return render_template('plans.html',  title='Маршруты')
    return redirect("/login")

@app.route('/liked')
def liked():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        liked_countries = None
        for el in users:
            if el == current_user:
                liked_countries = el.liked
        if not liked_countries:
            return render_template('no_liked.html', title='Избранное')
        li = liked_countries.split(', ')
        print(li)
        return render_template('liked.html', title='Избранное', countries=li)
    return redirect("/login")

@app.route('/create_plan')
def create_plan():
    return 'Создаю маршрут'


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/tourism')
def tourism():
    return render_template('tourism.html', title='Туризм')


@app.route('/advices')
def advices():
    return render_template('advices.html')

@app.route('/add_to_liked')
def add_to_liked():
    return 'Hello'


def main():
    db_session.global_init("db/mars_explorer.db")
    add_cities()
    app.run()


if __name__ == '__main__':
    main()