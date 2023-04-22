from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, make_response, g, session, flash, get_flashed_messages, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from random import shuffle
from datetime import datetime
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

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=True)
    psw = db.Column(db.String(500), nullable=True)
    email = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)
    city = db.Column(db.String(100))

    def __repr__(self):
        return f"<users {self.id}>"

@app.route("/")
def home(username=None):
    info = []
    try:
        info = Users.query.all()
    except:
        print("Ошибка чтения из БД")

    return render_template('home.html', title='Вечная зима', list=listLinks, info=info, username=session['username'])

@app.route("/contact", methods=("POST", "GET"))
def contact():
    if request.method == 'POST':
        try:
            user = Users.query.filter(Users.name == request.form['login']).all()
            if check_password_hash(user[0].psw, request.form['password']):
                session['username'] = user[0].name
                return redirect(url_for('home'))
            else:
                flash("Неверный логин или пароль")
        except:
            flash("Неверный логин или пароль")
    return redirect(url_for('home'))

@app.route('/disconnect')
def disconnect():
    session['username'] = None
    return redirect(url_for('home'))

@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        # здесь должна быть проверка корректности введенных данных
        try:
            hash = generate_password_hash(str(request.form['psw']))
            u = Users(name=request.form['name'], 
                    psw=hash, 
                    email=request.form['email'], 
                    age=request.form['age'], 
                    city=request.form['city'])
            db.session.add(u)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

        return redirect(url_for('home'))

    return render_template("register.html", title="Регистрация", list=listLinks)


if __name__ == "__main__":
    #with app.app_context():
    #    db.create_all()
    app.run(debug=True)