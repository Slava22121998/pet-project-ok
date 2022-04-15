from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index_page():
    if request.method == 'POST':
        fio_1 = request.form.get('fio_1')
        fio_2 = request.form.get('fio_2')
        fio_3 = request.form.get('fio_3')
        name_word_file = request.form.get('name_file')
        # create_words_file([fio_1, fio_2, fio_3], f'{name_word_file}')
        return render_template('duty_table_regular.html', tittle='Ответ сервера')
    else:
        return render_template('index.html', title='СЭБ ОК РКЗ "Ресурс"')


@app.route('/login/')
def login_page():
    return render_template('login.html', title='Войти в систему')


@app.route('/registration/')
def reg_page():
    return render_template('registration.html', title='Регистрация')


@app.route('/irregular_graph/', methods=['GET', 'POST'])
def irr_graph():
    if request.method == 'POST':
        input_count = int(request.form.get('input_count'))
        return redirect(url_for('irr_graph_for_count_employees', count=input_count))
    else:
        return render_template('employees_count.html', title='СЭБ ОК РКЗ "Ресурс"')


@app.route('/irregular_graph/employees/<int:count>/', methods=['GET', 'POST'])
def irr_graph_for_count_employees(count):
    if request.method == 'POST':
        pass
    else:
        return render_template('duty_table_irregular.html', count_input=count, title='Ненормированный график')


if __name__ == '__main__':
    app.run()
