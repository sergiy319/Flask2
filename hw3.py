from flask import Flask, render_template, request, make_response, session

# ДЗ 3. Счетчик открытий страницы. Простая авторизация пользователя.

"""
Создать 3 страницы `/`, `/login`, `/logout`:

 - Главная страница `/` будет отображать то сколько раз пользователь
 открывал страницу и какой юзер авторизовался на сайте(добавился в сессию)

 - Страница `/login` будет принимать два вида запросов GET и POST,
 когда только открываем страницу должна появится формочка для ввода юзернайма,
 после того как пользователь ввел никнейм формочку и нажал "Отправить",
 система должна добавить этого юзера в сессию, и вывести результат в теймлейте.
 Пример: "Пользователь зашел в систему как юзернейм". Если пользователь снова 
         захочет зайти на эту страничку и он залогинен,то вместо формочки должен 
         появится все тот же текст: "Пользователь зашел в систему как юзернейм"

 - Страница `/logout` должна чистить сессию если юзер авторизировался в системе
 
Количество теймплейтов не ограниченно
 
"""

# Инициализация приложения Flask
app = Flask(__name__)

# Для использования сессии во фласке указываем секретный ключ
app.secret_key = b'7f4hbc/k8'


@app.route('/')
def user_visit_count():
    visits = 0  # создаём переменную счетчика
    if request.cookies.get('visits'):  # проверяем наличие счетчика посещений в cookie переменной
        visits = int(request.cookies['visits'])  # Если такой параметр есть, транформируем его в число
    response = make_response(render_template('user_visit_count.html', visits=visits))  # передадаём счетчик в темлейт
    response.set_cookie('visits', str(visits + 1))  # увеличиваем значение счетчика на еденицу
    return response


@app.route('/login', methods=['GET', 'POST'])
def add_user():
    # узнаём тип запроса через request.method
    if request.method == 'GET':
        return render_template('add_user.html')  # создаём отображение формы
    elif request.method == 'POST':
        username = request.form['username']
        session['username'] = username  # создаём сохранение сессии
        return f'<h1>You have written your username: {username}</h1>'


@app.route('/logout')  # Страница "/logout" чистит сессию если юзер авторизировался в системе.
def clean_session():
    number_visits = 0  # создаём счётчик количества посещений
    if session.get('visits'):  # проверяем существует ли уже счетчик посещений в сессии
        number_visits = int(session['visits'])  # если существует - перезаписываем переменную счетчика
    else:
        session['visits'] = 0  # если не существует - создаем счетчик в сессии
    response = make_response(render_template('clean_session.html', visits=number_visits))

    session['visits'] += 1  # увеличиваем значение счетчика на еденицу
    return response


if __name__ == '__main__':
    app.run(debug=True)
