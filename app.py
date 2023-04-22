from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, make_response, g, session, flash, get_flashed_messages, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import util
from random import shuffle
from datetime import datetime
from sqlite3 import Binary
app = Flask(__name__)

app.config['SECRET_KEY'] = 'as8fr7s89fyfyas8f97f8afdfdsfgh9dsugri654kter9af3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///table.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


listLinks = [{'caption':'Главная', 'url':'/'},
            {'caption':'Мои многие нелепые мысли', 'url': '/news'},
            {'caption':'Результаты моего кризиса', 'url': '/pictures'},
            {'caption':'Хорошие опросы', 'url': '/survey'},
            {'caption': 'Полезные калькуляторы', 'url': '/calc'},
            {'caption': 'Интересные викторины', 'url': '/quiz'},
            {'caption': 'Магазин пустоты', 'url': '/shop'},
            {'caption': 'Любимые тексты', 'url': '/texts'},
            {'caption': 'Любимые песни', 'url': '/songs'},
            {'caption': 'Чат со снежным королем', 'url': '/kingchat'},
            {'caption': 'Ваш профиль', 'url': '/profile'}]

def getPageTitle(location):
    pageTitle=''
    for i in listLinks:
        if i['url'] == location:
            pageTitle = i['caption']
            return pageTitle
    return pageTitle

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=True, unique=True)
    psw = db.Column(db.String(500), nullable=True)
    email = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)
    city = db.Column(db.String(100))
    picture = db.Column(db.LargeBinary, nullable=True)
    __tablename__ = 'user'

    def __repr__(self):
        return f"<users {self.id}>"


@app.route("/")
def home(username=None):
    session['location'] = 'home'
    info = []
    info = Users.query.all()
    pageTitle = getPageTitle("/")
    return render_template('home.html', title='Вечная зима', list=listLinks, info=info, username=session['username'], pageTitle=pageTitle)

@app.route("/news")
def news(username=None):
    session['location'] = 'news'
    pageTitle = getPageTitle("/news")
    return render_template('news.html', title='Вечная зима', list=listLinks, username=session['username'], pageTitle=pageTitle)

@app.route("/userAva")
def userAva():
    user = Users.query.filter(Users.name == session['username']).all()
    pict = user[0].picture #request.files['picture'].read()
    if not pict:
        p = url_for('static', filename = 'empty.png')[1:]
        p = "D:/EternalWinter/static/empty.png"
        try:
            with open(p, 'rb') as file:
                pict = file.read()
        except FileNotFoundError:
            print('Аватарка по умолчанию не найдена')
    h = make_response(pict)
    h.headers['Content-Type'] = 'image\png'
    return h

@app.route("/upload", methods=("POST", "GET"))
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('Файл не выбран')
        else:
            avatar = file.read()
            avatar = Binary(avatar)
            user = Users.query.filter(Users.name == session['username']).all()
            user[0].picture = avatar
            db.session.commit()
        return redirect(url_for('profile'))

@app.route("/contact", methods=("POST", "GET"))
def contact():
    if request.method == 'POST':
        try:
            user = Users.query.filter(Users.name == request.form['login']).all()
            if check_password_hash(user[0].psw, request.form['password']):
                session['username'] = user[0].name
                return redirect(url_for(session['location']))
            else:
                flash("Неверный логин или пароль")
        except:
            flash("Неверный логин или пароль")
    return redirect(url_for(session['location']))

@app.route('/disconnect')
def disconnect():
    session['username'] = None
    return redirect(url_for(session['location']))

@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        # здесь должна быть проверка корректности введенных данных
        #try:
        hash = generate_password_hash(str(request.form['psw']))
        u = Users(name=request.form['name'], 
                psw=hash, 
                email=request.form['email'], 
                age=request.form['age'], 
                city=request.form['city'],
                picture=None)
        db.session.add(u)
        db.session.commit()
        #except:
        #    db.session.rollback()
        #    print("Ошибка добавления в БД")

        return redirect(url_for('home'))

    return render_template("register.html", title="Регистрация", list=listLinks)

@app.route("/profile")
def profile(username=None):
    if session['username']:
        session['location'] = 'profile'
        pageTitle = getPageTitle("/profile")
        user = Users.query.filter(Users.name == session['username']).all()
        return render_template('profile.html', title='Вечная зима', list=listLinks, username=session['username'], pageTitle=pageTitle, user=user)
    else:
        return redirect(url_for('home'))


@app.errorhandler(404)
def error1(error):
    session['location'] = 'error2'
    return render_template('error.html', title='Ошибка', list=listLinks, username=None, pageTitle='Страница не найдена')

@app.route('/error2')
def error2():
    return render_template('error.html', title='Ошибка', list=listLinks, username=None, pageTitle='Страница не найдена')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)