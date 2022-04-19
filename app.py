from flask import Flask, request, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from utils import get_fio_of_employees, set_data_of_employees_in_report_card

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '55a9a636bbd25522bae0e3fc967aa50a93649728'
app.permanent_session_lifetime = 24 * 3600

db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(125), nullable=False, unique=True)
    psw = db.Column(db.String(125), nullable=False)
    phone = db.Column(db.String(125), nullable=False)
    unit = db.Column(db.String(255), nullable=False)
    force = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'users-{self.id}'


@app.route('/', methods=['GET', 'POST'])
def index_page():
    if request.method == 'POST':
        fio_1 = request.form.get('fio-1')
        fio_2 = request.form.get('fio-2')
        fio_3 = request.form.get('fio-3')
        # print(fio_1, fio_2, fio_3)
        return render_template('response_of_server.html', title='Ответ сервера', authorization=True)
    else:
        if 'logged' in session:
            fio_list = get_fio_of_employees(Users.query.filter_by(name=session.get('logged')).all()[0].force)
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
                    session['logged'] = item.name
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
    db.create_all()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        unit = request.form.get('f')
        psw = generate_password_hash(request.form.get('psw'))  # Хэшируем пароль
        info_about_emp = request.form.get('info_about_employees')
        users = Users(name=name, email=email, phone=phone, psw=psw, unit=unit, force=info_about_emp)
        users_email = [x.email for x in db.session.query(
            Users.email).distinct()]  # Получаем список, в котором хранятся почты пользователей
        if email not in users_email:
            db.session.add(users)
            db.session.commit()
            session['logged'] = name
            return redirect('/')
        else:
            return 'Пользователь с таким email уже существует'

    else:
        return render_template('registration.html', title='Регистрация')


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
        Users.query.filter_by(name=session.get('logged')).all()[0].force), authorization=True)


@app.route('/user/<username>/')
def user_page(username):
    try:
        res = Users.query.all()
        unit = Users.query.filter_by(name=session.get('logged')).all()[0].unit
        # print(res)
        return render_template('user_page.html', title='Личный кабинет', unit=unit, info=res, authorization=True)
    except Exception as error:
        print(error)
        return 'Ошибка чтения из БД'


@app.route(f'/report_card/', methods=['GET', 'POST'])
def report_card_page():
    fio_list = get_fio_of_employees(
        Users.query.filter_by(name=session.get('logged')).all()[0].force)
    fio_list_size = len(fio_list)
    if request.method == 'POST':
        duty_days_of_employees_dict = dict()
        for i in range(1, fio_list_size + 1):
            duty_days_of_employees_dict[request.form.get(f'fio-{i}')] = (request.form.get(f'date-{i}')).split(',')
        set_data_of_employees_in_report_card(duty_days_of_employees_dict)
        return render_template('response_of_server.html', title='Ответ сервера', authorization=True)

    return render_template('report_card.html', title='Табель учета рабочего времени', fio_list=fio_list,
                           size=fio_list_size, authorization=True)


if __name__ == '__main__':
    app.run()
