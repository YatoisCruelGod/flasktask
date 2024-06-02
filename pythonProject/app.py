from flask import Flask, render_template, request, redirect, url_for, flash
import datetime
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from model import client1, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return client1.query.get(int(user_id))


@app.route('/')
def info():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    else:
        return render_template('main.html')

@app.route('/main')
def go_main():
    return render_template('main.html')
@app.route('/facts')
def facts():
    return render_template('gag.html')


@app.route('/sovet')
def sov():
    return render_template('boba.html')
@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = client1.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('user'))
        else:
            flash('Неверный логин или пароль')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = client1.query.filter_by(username=username).first()
        if user:
            flash('Это имя пользователя уже занято, придумайте другое')
        else:
            hashed_password = generate_password_hash(password)
            new_user = client1(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Аккаунт успешно создан')
            return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/user')
def user():
    if current_user.is_authenticated:
        return render_template('user.html', user=current_user)
    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
