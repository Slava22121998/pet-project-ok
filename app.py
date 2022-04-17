from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    force = db.Column(db.String(300), nullable=False)
    psw = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'Users-{self.id}'


class Employees(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    force = db.Column(db.String(300), nullable=False)
    employees = db.Column(db.TEXT, nullable=False)

    def __repr__(self):
        return f'Employees-{self.id}'


@app.route('/', methods=['GET', 'POST'])
def index_page():
    if request.method == 'POST':
        fio_1 = request.form.get('fio_1')
        fio_2 = request.form.get('fio_2')
        fio_3 = request.form.get('fio_3')
        name_word_file = request.form.get('name_file')
        return render_template('duty_table_regular.html', tittle='Ответ сервера')
    else:
        return render_template('index.html', title='СЭБ ОК РКЗ "Ресурс"')


@app.route('/login/')
def login_page():
    return render_template('login.html', title='Войти в систему')


@app.route('/registration/', methods=['GET', 'POST'])
def reg_page():
    if request.method == 'POST':
        db.create_all()
        email = request.form.get('email')
        phone = request.form.get('phone')
        force = request.form.get('f')
        psw = request.form.get('psw')
        info_about_emp = request.form.get('info_about_employees')
        users = Users(email=email, phone=phone, force=force, psw=psw)
        employees = Employees(force=force, employees=info_about_emp)
        try:
            db.session.add(users)
            db.session.add(employees)
            db.session.commit()
            return redirect(url_for('index_page'))
        except:
            return 'Ошибка при регистрации!'
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


if __name__ == '__main__':
    app.run()
