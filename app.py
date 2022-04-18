from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from utils import get_fio_of_employees

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '55a9a636bbd25522bae0e3fc967aa50a93649728'

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
        pass
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
        remember_me = request.form.get('ch_b')
        res = Users.query.all()
        for item in res:
            if item.email == email and check_password_hash(item.psw, password):
                if 'logged' not in session:
                    session['logged'] = item.name
                    if remember_me:
                        session.permanent = True
                    return redirect('/')
                else:
                    return 'Вы уже авторизованы!'

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


@app.route('/irregular_graph/', methods=['GET', 'POST'])
def irr_graph():
    if request.method == 'POST':
        input_count = int(request.form.get('input_count'))
        return redirect(url_for('irr_graph_for_count_employees', count=input_count))
    else:
        return render_template('employees_count.html', title='Количество сотрудников')


@app.route('/irregular_graph/employees/<int:count>/', methods=['GET', 'POST'])
def irr_graph_for_count_employees(count):
    if request.method == 'POST':
        data = dict()
        for i in range(count):
            data[request.form.get(f'fio-{i}')] = request.form.get(f'date-{i}')
        print(data)
        return "Hello"
    else:
        return render_template('duty_table_irregular.html', count_input=count, title='Ненормированный график')


@app.route('/user/<username>/')
def user_page(username):
    try:
        res = Users.query.all()
        print(res)
        return render_template('user_page.html', title='Личный кабинет', info=res, authorization=True)
    except Exception as error:
        print(error)
        return 'Ошибка чтения из БД'


if __name__ == '__main__':
    app.run()
