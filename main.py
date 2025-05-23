import datetime
import logging
import os
import sqlite3
from flask import Flask, render_template, redirect, request
from data import db_session
from data.cities import City
from data.plans import Plan
from data.users import User
from data.airports import Airport
from data.russian_cities import RussianCity
from data.countries import Country
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.user import RegisterForm, LoginForm, ProfileForm, AddPhotoForm
from forms.fly import FlyForm


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


def add_airports():
    con = sqlite3.connect('db/travel.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT name FROM cities""").fetchall()
    con.close()
    result = [i[0] for i in result]
    russia = ['Москва', 'Санкт-Петербург', 'Казань', 'Сочи', 'Петрозаводск(Карелия)', 'Петропавловск-Камчатский(Камчатка)',
              'Минеральные воды(Кисловодск)', 'Симферополь(Крым)', 'Владивосток', 'Калининград', 'Махачкала(Дербент)']
    cities = russia + result
    names = ['MOW', 'LED', 'KZN', 'AER', 'PES', 'PKC', 'MRV', 'SIP', 'VVO', 'KGD', 'MCX', 'AYT', 'IST', 'MAD', 'BCN',
             'SPX', 'HRG']
    db_sess = db_session.create_session()
    con = sqlite3.connect('db/travel.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT city FROM airports""").fetchone()
    con.close()
    if not result:
        for i in range(len(cities)):
            airport = Airport(
                city=cities[i],
                name=names[i]
            )
            db_sess.add(airport)
    db_sess.commit()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/fly', methods=['GET', 'POST'])
def fly():
    form = FlyForm()
    if form.validate_on_submit():
        start = form.start.data
        finish = form.finish.data
        con = sqlite3.connect('db/travel.db')
        cur = con.cursor()
        start_link = cur.execute(f"""SELECT name FROM airports WHERE city = ?""", (start,)).fetchone()[0]
        finish_link = cur.execute(f"""SELECT name FROM airports WHERE city = ?""", (finish,)).fetchone()[0]
        con.close()
        start_date = [int(i) for i in str(form.start_date.data).split('-')]
        end_date = [int(i) for i in str(form.end_date.data).split('-')]
        now_date = [int(i) for i in str(datetime.date.today()).split('-')]
        year_later_date = [int(i) for i in str(datetime.date.today() + datetime.timedelta(days=364)).split('-')]
        if start == finish:
            return render_template('fly.html', title='Авиабилеты',
                                   form=form,
                                   message="Пункт отправления не может быть равен пункту назначения")
        elif start_date < now_date:
            return render_template('fly.html', title='Авиабилеты',
                                   form=form,
                                   message="Дата отправления не может быть раньше текущей даты")
        elif start_date > year_later_date:
            return render_template('fly.html', title='Авиабилеты',
                                   form=form,
                                   message="Дата отправления должна быть в пределах года с текущего дня")
        elif end_date > year_later_date:
            return render_template('fly.html', title='Авиабилеты',
                                   form=form,
                                   message="Дата возвращения должна быть в пределах года с текущего дня")
        elif start_date > end_date:
            return render_template('fly.html', title='Авиабилеты',
                                   form=form,
                                   message="Дата возвращения не может быть меньше даты отправления")
        else:
            ost1 = '0' * (2 - len(str(start_date[2])))
            ost2 = '0' * (2 - len(str(start_date[1])))
            start_date_link = ost1 + str(start_date[2]) + ost2 + str(start_date[1])
            ost1 = '0' * (2 - len(str(end_date[2])))
            ost2 = '0' * (2 - len(str(end_date[1])))
            end_date_link = ost1 + str(end_date[2]) + ost2 + str(end_date[1])
            start_date_new = [str(start_date[0])] + ['0' * (2 - len(str(i))) + str(i) for i in start_date if len(str(i)) <= 2]
            end_date_new = [str(end_date[0])] + ['0' * (2 - len(str(i))) + str(i) for i in end_date if len(str(i)) <= 2]
            start_date_new = '.'.join(start_date_new[::-1])
            end_date_new = '.'.join(end_date_new[::-1])
            adult = form.adult.data
            child = form.child.data
            baby = form.baby.data
            if child == '':
                child = '0'
            if baby == '':
                baby = '0'
            if not adult.isnumeric() or not child.isnumeric() or not baby.isnumeric():
                return render_template('fly.html', title='Авиабилеты',
                                       form=form,
                                       message="Кол-во пассажиров должно быть неотрицательным числом(или пустой строкой)")
            elif int(adult) < 0 or int(baby) < 0 or int(child) < 0:
                return render_template('fly.html', title='Авиабилеты',
                                       form=form,
                                       message="Кол-во пассажиров должно быть неотрицательным числом(или пустой строкой)")
            elif int(adult) < 1:
                return render_template('fly.html', title='Авиабилеты',
                                       form=form,
                                       message="Кол-во взрослых не может быть менее одного")
            if child == '0':
                child_link = ''
            else:
                child_link = child
            if baby == '0':
                baby_link = ''
            else:
                baby_link = baby
            clas = form.clas.data
            if clas != 'Эконом':
                if clas == 'Комфорт':
                    clas_link = 'w'
                elif clas == 'Бизнес':
                    clas_link = 'c'
                elif clas == 'Первый класс':
                    clas_link = 'f'
            else:
                clas_link = ''
            global link
            link = f'https://www.aviasales.ru/search/?params={start_link}{start_date_link}{finish_link}{end_date_link}{clas_link}{adult}{child_link}{baby_link}'
            return redirect(f'/find_tickets/{start}--{finish}--{start_date_new}--{end_date_new}--{adult}--{child}--{baby}--{clas}')
    return render_template('fly.html', title='Авиабилеты', form=form)


@app.route('/find_tickets/<start>--<finish>--<start_date>--<end_date>--<adult>--<child>--<baby>--<clas>')
def find_tickets(start, finish, start_date, end_date, adult, child, baby, clas):
    return render_template('find_tickets.html', title='Смотреть билеты', link=link, start=start, finish=finish, start_date=start_date,
                           end_date=end_date, adult=adult, child=child, baby=baby, clas=clas)


@app.route('/russian_cities')
def russian_cities():
    con = sqlite3.connect('db/travel.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT city FROM russian_cities""").fetchall()
    con.close()
    cities = [i[0] for i in result]
    return render_template('russian_cities.html', title='Россия', cities=cities)


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
    return render_template('main.html',  title='Главная')


@app.route('/countries')
def choose_countries():
    db_sess = db_session.create_session()
    li_countries = db_sess.query(Country.name).all()
    all_countries = [x[0] for x in li_countries]
    return render_template('countries.html',  title='Страны', countries=all_countries)


@app.route(f'/country/<name>')
def country(name):
    db_sess = db_session.create_session()
    li_cities = db_sess.query(Country).filter(Country.name == name).first()
    li_cities = li_cities.cities.split(',')
    d = {}
    for el in li_cities:
        city = db_sess.query(City).filter(City.name == el).first()
        tourism = city.tourism
        text = city.text
        d[tourism] = d.get(tourism, []) + [(el, text)]
    return render_template(f'country.html', title=name, name=name,
                           relax=d.get('Рекреационный', []),
                           culture=d.get('Культурный', ''),
                           active=d.get('Активный', ''))


@app.route('/map/<word>/<name>')
def download_map(word, name):
    from search import search_for_map
    search_for_map(name)
    return redirect(f'/opened_map/{name}')


@app.route('/opened_map/<name>')
def open_map(name):
    return render_template('opened_map.html', name=name,  title='Карта')


@app.route('/map/tourism/<word>/<name>')
def open_map_tourism(word, name):
    from search import search_for_map
    search_for_map(name)
    return redirect(f'/opened_map/{name}')


@app.route('/my_profile', methods=['POST', 'GET'])
def my_profile():
    if current_user.is_authenticated:
        form = ProfileForm(
            email=current_user.email,
            surname=current_user.surname,
            name=current_user.name,
            age=current_user.age
        )
        if request.method == 'GET':
            return render_template('profile.html', title='Мой профиль', form=form)
        elif request.method == 'POST':
            current_user.email = form.email.data
            current_user.surname = form.surname.data
            current_user.name = form.name.data
            current_user.age = form.age.data
            db_sess = db_session.create_session()
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/my_profile')
    return redirect("/login")


@app.route('/my_plans')
def my_plans():
    if current_user.is_authenticated:
        plans = current_user.plans
        if not plans:
            return render_template('no_plans.html', title='Маршруты')
        li = plans.split(',')
        return render_template('plans.html',  title='Маршруты', plans=li)
    return redirect("/login")


@app.route('/plan/<word>')
def open_plan(word):
    db_sess = db_session.create_session()
    id = current_user.id
    plans = db_sess.query(Plan.cities).filter(Plan.name == word, Plan.user_id == id).first()
    plans = plans[0].split(',')
    return render_template("open_plan.html", title=word, cities=plans, plan=word)


@app.route('/photos/<word>')
def open_photos(word):
    id = current_user.id
    if os.path.exists(f'static/img/{word}_{current_user.id}'):
        photos = os.listdir(f'static/img/{word}_{current_user.id}')
    else:
        os.mkdir(f'static/img/{word}_{current_user.id}')
        photos = None
    if photos:
        return render_template("open_photos.html", title='Мои фото', photos=photos, word=word, id=id)
    return redirect(f'/add_photo/{word}')


@app.route('/add_photo/<word>', methods=['POST', 'GET'])
def add_photos(word):
    form = AddPhotoForm()
    if form.validate_on_submit():
        if os.path.exists(f'static/img/{word}_{current_user.id}'):
            photos = os.listdir(f'static/img/{word}_{current_user.id}')
            k = len(photos) + 1
        else:
            os.mkdir(f'static/img/{word}_{current_user.id}')
            k = 1
        f = form.img.data
        with open(f'static/img/{word}_{current_user.id}/{k}.png', 'wb') as file_in:
            data = f.read()
            file_in.write(data)
        return redirect(f'/photos/{word}')
    return render_template('add_photos.html', form=form, title='Выберите фото')

@app.route('/liked')
def liked():
    if current_user.is_authenticated:
        liked_countries = current_user.liked_countries
        liked_cities = current_user.liked_cities
        if not liked_countries and not liked_cities:
            return render_template('no_liked.html', title='Избранное')
        li_countries = []
        li_cities = []
        if liked_countries:
            li_countries = liked_countries.split(',')
        if liked_cities:
            li_cities = liked_cities.split(',')
        return render_template('liked.html', title='Избранное', countries=li_countries, cities=li_cities)
    return redirect('/login')


@app.route('/create_plan', methods=['POST', 'GET'])
def create_plan():
    db_sess = db_session.create_session()
    cities = db_sess.query(City.name).all()
    cities_new = [x[0] for x in cities]
    russian_cities = db_sess.query(RussianCity.city).all()
    russian_cities_new = [x[0] for x in russian_cities]
    list_cities = cities_new + russian_cities_new
    selected_city = []
    plans = current_user.plans
    id = current_user.id
    if request.method == 'GET':
        return render_template('create_plan.html', title='Создаю маршрут', cities=list_cities)
    elif request.method == 'POST':
        name = request.form['name']
        name = name.strip()
        if not name:
            return render_template('create_plan.html', title='Создаю маршрут', cities=list_cities,
                                   message="Имя не должно быть пустым")
        db_sess = db_session.create_session()
        if db_sess.query(Plan).filter(Plan.name == name, Plan.user_id == id).first():
            return render_template('create_plan.html', title='Создаю маршрут', cities=list_cities,
                                   message="Маршрут с таким именем уже есть")
        if plans:
            plans += f',{name}'
        else:
            plans = name
        current_user.plans = plans
        db_sess.merge(current_user)
        db_sess.commit()
        for el in list_cities:
            try:
                selected_city.append(request.form[el])
            except:
                continue
        plan = Plan(
            name=name,
            cities=','.join(selected_city),
            user_id = id
        )
        db_sess.add(plan)
        db_sess.commit()
        return render_template('plan_ready.html', title='Добавлен')


@app.route('/add_to_plan/<word>/<city>', methods=['POST', 'GET'])
def add_to_plan(word, city):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        id = current_user.id
        plans = db_sess.query(Plan.name).filter(Plan.user_id == id).all()
        li_plans = [x[0] for x in plans]
        if not li_plans:
            return render_template('no_plans.html', title='Маршруты')
        selected_plans = []
        if request.method == 'GET':
            return render_template('add_to_plan.html', title='Добавляем', plans=li_plans)
        elif request.method == 'POST':
            for el in li_plans:
                try:
                    selected_plans.append(request.form[el])
                except:
                    continue
            for el in selected_plans:
                plan = db_sess.query(Plan).filter(Plan.name == el, Plan.user_id == id).first()
                new_cities = plan.cities
                if city not in new_cities:
                    new_cities += f',{city}'
                plan.cities = new_cities
                db_sess.merge(plan)
                db_sess.commit()
            return redirect(f'/{word}')
    return redirect('/login')


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
            email=form.email.data,
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
    return render_template('tourism_type.html', title="Туризм", cities=cities, type=type, word=word)


@app.route('/add_to_liked_country/<word>/<country>')
def add_to_liked(word, country):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        liked_countries = current_user.liked_countries
        if not liked_countries:
            liked_countries = country
        else:
            if country not in liked_countries:
                liked_countries += f',{country}'
        current_user.liked_countries = liked_countries
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect(f'/{word}')
    return redirect('/login')


@app.route('/add_to_liked_city/<word>/<country>')
def add_to_liked_city(word, country):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        liked_cities = current_user.liked_cities
        if not liked_cities:
            liked_cities = country
        else:
            if country not in liked_cities:
                liked_cities += f',{country}'
        current_user.liked_cities = liked_cities
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect(f'/{word}')
    return redirect('/login')


@app.route('/add_to_liked_city/country/<word>/<country>')
def add_to_liked_city_in_country(word, country):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        liked_cities = current_user.liked_cities
        if not liked_cities:
            liked_cities = country
        else:
            if country not in liked_cities:
                liked_cities += f',{country}'
        current_user.liked_cities = liked_cities
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect(f'/country/{word}')
    return redirect('/login')


@app.route('/add_to_liked_city_from_tourism/tourism/<word>/<country>')
def add_to_liked_city_from_tourism(word, country):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        liked_cities = current_user.liked_cities
        if not liked_cities:
            liked_cities = country
        else:
            if country not in liked_cities:
                liked_cities += f',{country}'
        current_user.liked_cities = liked_cities
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect(f'/tourism/{word}')
    return redirect('/login')


@app.route('/remove_from_liked/<country>')
def remove_from_liked(country):
    db_sess = db_session.create_session()
    liked_countries = current_user.liked_countries
    liked_cities = current_user.liked_cities
    if liked_countries:
        liked_countries = liked_countries.split(',')
    else:
        liked_countries = []
    if liked_cities:
        liked_cities = liked_cities.split(',')
    else:
        liked_cities = []
    if country in liked_countries:
        i = liked_countries.index(country)
        del liked_countries[i]
        current_user.liked_countries = ','.join(liked_countries)
    else:
        i = liked_cities.index(country)
        del liked_cities[i]
        current_user.liked_cities = ','.join(liked_cities)
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect('/liked')


@app.route('/delete_from_plan/<name>/<city>')
def delete_from_plan(name, city):
    db_sess = db_session.create_session()
    id = current_user.id
    plan = db_sess.query(Plan).filter(Plan.user_id == id, Plan.name == name).first()
    cities = plan.cities
    cities = cities.split(',')
    i = cities.index(city)
    del cities[i]
    plan.cities = ','.join(cities)
    db_sess.merge(plan)
    db_sess.commit()
    return redirect(f'/plan/{name}')


@app.route('/delete_plan/<name>')
def delete_plan(name):
    db_sess = db_session.create_session()
    id = current_user.id
    plans = current_user.plans
    plans = plans.split(',')
    i = plans.index(name)
    del plans[i]
    current_user.plans = ','.join(plans)
    db_sess.merge(current_user)
    db_sess.commit()
    plan = db_sess.query(Plan).filter(Plan.user_id == id, Plan.name == name).first()
    db_sess.delete(plan)
    db_sess.commit()
    return redirect('/my_plans')


def main():
    db_session.global_init("db/travel.db")
    add_cities()
    add_airports()
    app.run()


if __name__ == '__main__':
    main()