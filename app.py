from datetime import datetime

from flask import Flask, request, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from utils import get_fio_of_employees, get_data_about_employees, set_data_of_employees_in_report_card

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '55a9a636bbd25522bae0e3fc967aa50a93649728'
app.permanent_session_lifetime = 24 * 3600

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    login = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(125), nullable=False, unique=True)
    psw = db.Column(db.String(125), nullable=False)
    phone = db.Column(db.String(125), nullable=False, unique=True)
    unit = db.Column(db.String(255), nullable=False, unique=True)
    force = db.Column(db.Text, nullable=False)

    employ = db.relationship('Employees', backref='users', lazy=True)

    def __repr__(self):
        return f'users-{self.id}'


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    unit = db.Column(db.String, db.ForeignKey('users.unit'), nullable=False)
    duty_days = db.Column(db.String, default='Дни дежурств не заполнены')
    datetime = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<employees-{self.id}>'


@app.route('/', methods=['GET', 'POST'])
def index_page():
    if request.method == 'POST':
        fio_1 = request.form.get('fio-1')
        fio_2 = request.form.get('fio-2')
        fio_3 = request.form.get('fio-3')
        employees = get_data_about_employees([fio_1, fio_2, fio_3])
        for fio, dates in employees.items():
            employees = Employees(username=fio, unit=Users.query.filter_by(login=session.get('logged')).all()[0].unit,
                                  duty_days=",".join(dates))
            db.session.add(employees)
            db.session.commit()
        return render_template('response_of_server.html', title='Ответ сервера', authorization=True)

    else:
        if 'logged' in session:
            fio_list = get_fio_of_employees(Users.query.filter_by(login=session.get('logged')).all()[0].force)
            return render_template('index.html', title='СЭБ ОК РКЗ "Ресурс"', authorization=True, fio_list=fio_list)
        else:
            return render_template('index.html', title='СЭБ ОК РКЗ "Ресурс"', authorization=False)


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('psw')
        res = Users.query.all()
        for item in res:
            if item.email == email and check_password_hash(item.psw, password):
                if 'logged' not in session:
                    session['logged'] = item.login
                    return redirect('/')

        return 'Проблемы с авторизацией'

    else:
        return render_template('login.html')


@app.route('/logout/')
def logout_page():
    session.pop('logged', None)
    return redirect('/')


@app.route('/registration/', methods=['GET', 'POST'])
def reg_page():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        email = request.form.get('email')
        phone = request.form.get('phone')
        psw = generate_password_hash(request.form.get('psw'))  # Хэшируем пароль
        unit = request.form.get('unit')
        force = request.form.get('info_about_employees')

        users = Users(name=name, login=login, email=email, phone=phone, psw=psw, unit=unit, force=force)

        users_email = [x.email for x in db.session.query(
            Users.email).distinct()]  # Получаем уникальный список, в котором хранятся почты пользователей
        if email not in users_email:
            db.session.add(users)
            db.session.commit()
            session['logged'] = login
            return redirect('/')
        else:
            return 'Пользователь с таким email уже существует'

    else:
        return render_template('registration.html', title='Регистрация')


@app.route('/user/<username>/')
def user_page(username):
    try:
        res = Users.query.all()
        unit = Users.query.filter_by(login=session.get('logged')).all()[0].unit
        # print(res)
        return render_template('user_page.html', title='Личный кабинет', unit=unit, info=res, authorization=True,
                               name=Users.query.filter_by(login=session.get('logged')).all()[0].name)
    except Exception as error:
        print(error)
        return 'Ошибка чтения из БД'


@app.route('/create/unnormal_schedule/', methods=['GET', 'POST'])
def irr_graph_temp():
    if request.method == 'POST':
        employees_count = int(request.form.get('posts_count'))
        return redirect(url_for('irr_graph_result', count=employees_count))

    return render_template('unnormal_shedule_temp.html', authorization=True, title='Введите количество контролёров')


@app.route('/create/unnormal_schedule/persons/<int:count>', methods=['GET', 'POST'])
def irr_graph_result(count):
    if request.method == 'POST':
        fio_dict = dict()
        for i in range(1, count + 1):
            fio_dict[request.form.get(f'fio-{i}')] = ''.join(request.form.get(f'date-{i}'))
        print(fio_dict)
        return render_template('response_of_server.html', title='Ответ сервера', authorization=True)

    return render_template('unnormal_shedule.html', count=count, fio_list=get_fio_of_employees(
        Users.query.filter_by(login=session.get('logged')).all()[0].force), authorization=True)


@app.route(f'/report_card/', methods=['GET', 'POST'])
def report_card_page():
    date_dict = dict()

    for item in Users.query.filter_by(login=session.get('logged')).first().employ:
        date_dict[item.username] = item.duty_days.split(',')

    set_data_of_employees_in_report_card(date_dict, Users.query.filter_by(login=session.get('logged')).first().unit)

    return render_template('response_of_server.html', title='Ответ сервера', authorization=True)

if __name__ == '__main__':
    app.run()
