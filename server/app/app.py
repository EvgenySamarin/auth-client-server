#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask
from flask.helpers import url_for, redirect, flash, abort
from flask.globals import session, request
from flask.templating import render_template
from werkzeug.security import generate_password_hash

from utils import print_debug
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# connect app to SQLAlchemy SQLite
alchemy_database = SQLAlchemy(app)


class Users(alchemy_database.Model):
    """ User storage class to save data into SQLAlchemy's table the same name """
    id = alchemy_database.Column(alchemy_database.Integer, primary_key=True)
    login = alchemy_database.Column(alchemy_database.String(50), unique=True)
    email = alchemy_database.Column(alchemy_database.String(50), unique=True)
    psw = alchemy_database.Column(alchemy_database.String(500), nullable=True)
    date = alchemy_database.Column(alchemy_database.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<users {self.id}, {self.email}, {self.psw}, {self.date}>"


class Profiles(alchemy_database.Model):
    """ Profile storage class to save data into SQLAlchemy's table the same name """
    id = alchemy_database.Column(alchemy_database.Integer, primary_key=True)
    name = alchemy_database.Column(alchemy_database.String(50), nullable=True)
    old = alchemy_database.Column(alchemy_database.Integer)
    city = alchemy_database.Column(alchemy_database.String(100))

    user_id = alchemy_database.Column(alchemy_database.Integer, alchemy_database.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"


class Mainmenu(alchemy_database.Model):
    """ Mainmenu storage class to save data into SQLAlchemy's table the same name """
    id = alchemy_database.Column(alchemy_database.Integer, primary_key=True)
    title = alchemy_database.Column(alchemy_database.String(50), unique=True)
    url = alchemy_database.Column(alchemy_database.String(50), nullable=True)

    def __repr__(self):
        return f"<mainmenu {self.id}>"


def fill_mainmenu():
    alchemy_database.session.add(Mainmenu(title="Main", url="/index"))
    alchemy_database.session.add(Mainmenu(title="Sign-In", url="/auth"))
    alchemy_database.session.add(Mainmenu(title="About", url="/about"))
    alchemy_database.session.add(Mainmenu(title="Auth-logs", url="/logs"))
    alchemy_database.session.add(Mainmenu(title="Sign-out", url="/signout"))
    alchemy_database.session.commit()


def get_menu():
    if is_user_login():
        return Mainmenu.query.all()
    else:
        return Mainmenu.query.filter(Mainmenu.url != "/signout").all()


@app.route('/index')
@app.route('/')
def index():
    """
    Rander main page
    """
    print_debug(application=app, message=url_for('index'))
    print("session key is " + app.config['SECRET_KEY'])

    return render_template(
        'index.html',
        title="Main",
        header="Main page",
        menu=get_menu(),
    )


@app.route('/auth', methods=["POST", "GET"])
def auth():
    """
    Render login page
    """
    print_debug(application=app, message=url_for('auth'))

    if is_user_login():
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == "POST" and request.form['login'] == "user" and request.form['password'] == "1234":
        session['userLogged'] = request.form['login']

        try:
            hash_psw = generate_password_hash(request.form['password'])
            new_row = Users(login=request.form['login'], psw=hash_psw)
            alchemy_database.session.add(new_row)
            # flush needed to use new appended table row in other request. Here just for example
            alchemy_database.session.flush()
            alchemy_database.session.commit()
            return redirect(url_for('profile', username=session['userLogged']))
        except:
            alchemy_database.session.rollback()
            flash("Ошибка записи логов в БД", category='error')

    if request.method == "POST":
        if not request.form["login"] or not request.form["password"]:
            flash("Нечего отправлять", category='error')
        else:
            try:
                hash_psw = generate_password_hash(request.form['password'])
                new_row = Users(login=request.form['login'], psw=hash_psw)
                alchemy_database.session.add(new_row)
                alchemy_database.session.commit()
                flash("Попытка входа записана в БД", category='success')
            except:
                alchemy_database.session.rollback()
                flash("Ошибка записи логов в БД", category='error')
        print_debug(application=app, message=request.form)

    return render_template(
        'auth.html',
        title="Log-in",
        header="Authorization",
        menu=get_menu(),
    )


def is_user_login() -> bool:
    return 'userLogged' in session


@app.route('/profile/<username>')
def profile(username):
    """
    Render profile page

    :param username: current username
    """
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return render_template(
        'profile.html',
        title="Profile",
        header=f"Profile {username}",
        menu=get_menu(),
        username=username,
    )


@app.route('/signout')
def sign_out():
    """
    Clear user session and redirect
    """
    if is_user_login():
        session.clear()
        redirect(url_for('index'))
    else:
        # unexpected error sign_out must be visible only for authorized user
        abort(500)
    return index()


@app.route('/about')
def about():
    """
    Render about page
    """
    print_debug(application=app, message=url_for('about'))
    return render_template(
        'about.html',
        title="About us",
        header="About site",
        menu=get_menu(),
    )


@app.route('/logs')
def logs():
    """
    Render database logs page
    """
    print_debug(application=app, message=url_for('logs'))

    return render_template(
        'logs.html',
        title="Logs",
        header="",
        menu=get_menu(),
        logs=Users.query.all(),
    )


@app.errorhandler(404)
def page_not_found(error):
    """
    Render error page not found
    """
    print_debug(application=app, message=error)
    return render_template(
        'error.html',
        title="Page not found",
        header="Error",
        menu=get_menu(),
    ), 404


@app.errorhandler(401)
def page_not_found(error):
    """
    Render error page unauthorized
    """
    print_debug(application=app, message=error)

    return render_template(
        'error.html',
        title="Page not found",
        header="Unauthorized",
        menu=get_menu(),
    ), 401


if __name__ == '__main__':
    # create SQLAlchemy database and fill Mainmenu if needed
    with app.app_context():
        alchemy_database.create_all()
        if len(Mainmenu.query.all()) == 0:
            fill_mainmenu()
    app.run(debug=True, host="0.0.0.0", port=4999)
