from flask import Flask, request, render_template

from utils import create_excel_file, create_words_file

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/duty_schedule', methods=['GET', 'POST'])
def duty_table_for_3():
    if request.method == 'POST':
        fio_1 = request.form.get('fio_1')
        fio_2 = request.form.get('fio_2')
        fio_3 = request.form.get('fio_3')
        create_excel_file([fio_1, fio_2, fio_3], 'post_1')
        create_words_file([fio_1, fio_2, fio_3], 'post_1')
    return render_template('duty_table_3.html')


if __name__ == '__main__':
    app.run()
