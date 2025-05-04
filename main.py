import datetime
import logging
import sqlite3
from flask import Flask, render_template, redirect, request
from data import db_session
from data.cities import City
from data.users import User
from data.russian_cities import RussianCity
from data.countries import Country
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import RegisterForm, LoginForm


app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
logging.basicConfig(
    filename='example.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.WARNING)


def add_cities():
    cities = [['Москва', 'Москва — город федерального значения.', 'Культурный'],
              ['Санкт-Петербург', 'Санкт-Петербург — город федерального значения.', 'Культурный'],
              ['Казань', 'Республика Татарстан', 'Культурный'], ['Сочи', 'Краснодарский край', 'Рекреационный, активный'],
              ['Карелия', 'Республика Карелия', 'Активный'], ['Камчатка', 'Камчатский край', 'Активный'],
              ['Кисловодск', 'Ставропольский край', 'Рекреационный'], ['Кавказ', '-', 'Активный'],
              ['Крым', 'Республика Крым', 'Рекрационный'], ['Владивосток', 'Приморский край', 'Культурный'],
              ['Калининград', 'Калининградская область', 'Культурный'], ['Дербент', 'Республика Дагестан', 'Рекреационный']]
    db_sess = db_session.create_session()
    con = sqlite3.connect('db/travel.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT city FROM russian_cities""").fetchone()
    con.close()
    if not result:
        for city in cities:
            city_bd = RussianCity(
                city=city[0],
                subject=city[1],
                tourism=city[2]
            )
            db_sess.add(city_bd)
    db_sess.commit()
    con = sqlite3.connect('db/travel.db')
    cur = con.cursor()
    cur.execute(f"""DELETE FROM russian_cities WHERE id > 12""")
    con.commit()
    con.close()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/russian_cities')
def russian_cities():
    con = sqlite3.connect('db/travel.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT city FROM russian_cities""").fetchall()
    con.close()
    cities = [i[0] for i in result]
    return render_template('russian_cities.html', title='Города России', cities=cities)


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


@app.route(f'/country/<name>')
def country(name):
    db_sess = db_session.create_session()
    li_cities = db_sess.query(Country).filter(Country.name == name).first()
    li_cities = li_cities.cities.split(',')
    d = {}
    for el in li_cities:
        tourism = db_sess.query(City).filter(City.name == el).first().tourism
        d[tourism] = d.get(tourism, []) + [el]
    return render_template(f'country.html', title=name,
                           relax=d.get('Рекреационный', []),
                           culture=d.get('Культурный', ''),
                           active=d.get('Активный', ''))


@app.route('/country/map/<name>')
def open_map(name):
    from search import search_for_map
    search_for_map(name)
    return ''


@app.route('/my_profile', methods=['POST', 'GET'])
def my_profile():
    if current_user.is_authenticated:
        return render_template('profile.html', title='Мой профиль')
    return redirect("/login")


@app.route('/my_plans')
def my_plans():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        plans = None
        for el in users:
            if el == current_user:
                plans = el.plans
                break
        print(plans)
        if not plans:
            return render_template('no_plans.html', title='Маршруты')
        li = plans.split(', ')
        return render_template('plans.html',  title='Маршруты', plans=li)
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
                break
        if not liked_countries:
            return render_template('no_liked.html', title='Избранное')
        li = liked_countries.split(',')
        return render_template('liked.html', title='Избранное', countries=li)
    return redirect('/login')


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


@app.route('/tourism/<word>')
def tourism_word(word):
    if word == 'beach':
        type = 'Рекреационный'
    elif word == 'active':
        type = 'Активный'
    else:
        type = 'Культурный'
    db_sess = db_session.create_session()
    result1 = db_sess.query(City.name).filter(City.tourism == type).all()
    con = sqlite3.connect('db/travel.db')
    cur = con.cursor()
    result2 = cur.execute(f"""SELECT city FROM russian_cities WHERE tourism = ?""", (type,)).fetchall()
    con.close()
    result = result1 + result2
    cities = [x[0] for x in result]
    '''result_russian = db_sess.query(RussianCity.city).filter(RussianCity.tourism == type).all()
    for el in result_russian:
        cities.append(el[0])'''
    return render_template('tourism_type.html', cities=cities)


@app.route('/advices')
def advices():
    return render_template('advices.html')


@app.route('/add_to_liked/<word>/<country>')
def add_to_liked(word, country):
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    liked_countries = None
    for el in users:
        if el == current_user:
            liked_countries = el.liked
            break
    if not liked_countries:
        liked_countries = country
    else:
        if country not in liked_countries:
            liked_countries += f',{country}'
    current_user.liked = liked_countries
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect(f'/{word}')


@app.route('/remove_from_liked/<country>')
def remove_from_liked(country):
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    liked_countries = None
    for el in users:
        if el == current_user:
            liked_countries = el.liked
            break
    liked_countries = liked_countries.split(',')
    i = liked_countries.index(country)
    del liked_countries[i]
    current_user.liked = ','.join(liked_countries)
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect('/liked')


def main():
    db_session.global_init("db/travel.db")
    add_cities()
    app.run()


if __name__ == '__main__':
    main()