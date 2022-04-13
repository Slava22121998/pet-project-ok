from flask import Flask, request, render_template

from utils import create_words_file

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index_page():
    if request.method == 'POST':
        fio_1 = request.form.get('fio_1')
        fio_2 = request.form.get('fio_2')
        fio_3 = request.form.get('fio_3')
        name_word_file = request.form.get('name_file')
        create_words_file([fio_1, fio_2, fio_3], f'{name_word_file}')
        return render_template('duty_table_3.html', tittle='Ответ сервера')
    else:
        return render_template('index.html', title='СЭБ ОК РКЗ "Ресурс"')


@app.route('/login')
def login_page():
    return render_template('login.html', title='Войти в систему')


@app.route('/registration')
def reg_page():
    return render_template('registration.html', title='Регистрация')


if __name__ == '__main__':
    app.run()
