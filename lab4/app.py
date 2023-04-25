import requests
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

# Инициализация Flask приложения
app = Flask(__name__)

# Установка соединения с базой данных
conn = psycopg2.connect(database="users",
                        user="postgres",
                        password="12345",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

# Обработка корневого маршрута и перенаправление на страницу входа
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))

# Обработка маршрута для страницы входа (GET запрос)
@app.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')

# Обработка маршрута для страницы входа (POST запрос)
@app.route('/login/', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    registration = request.form.get('registration')

    # Проверка нажатия кнопки "registration" и перенаправление на страницу регистрации
    if registration:
        return redirect(url_for('registration'))

    # Возвращение сообщений об ошибке, если логин или пароль не введены
    if not username:
        return render_template('login.html', error='Введите логин')
    if not password:
        return render_template('login.html', error='Введите пароль')

    # Выполнение запроса к базе данных для проверки существующих пользователей с указанными логином и паролем
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if records == []:
        return render_template('account.html')
    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])

# Обработка маршрута для страницы регистрации
@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        # Возвращение сообщений об ошибке, если имя пользователя, логин или пароль не введены
        if not name:
            return render_template('registration.html', error='Введите имя пользователя')
        if not login:
            return render_template('registration.html', error='Введите логин')
        if not password:
            return render_template('registration.html', error='Введите пароль')

        # Проверка наличия логина в базе данных
        cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(login),))
        if cursor.fetchone() is not None:
            return render_template('registration.html', error='Логин уже существует. Пожалуйста, выберите другой.')

        # Вставка новой записи в таблицу пользователей
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        # Перенаправление на страницу входа после успешной регистрации
        return redirect('/login/')

    return render_template('registration.html')

# Запуск приложения Flask с включенным режимом отладки
if __name__ == '__main__':
    app.run(debug=True)