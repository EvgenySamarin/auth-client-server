#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os
from flask.app import Flask
from flask.helpers import url_for, redirect, flash, abort
from flask.globals import session, request, g
from flask.templating import render_template
from utils import print_debug

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

main_menu = [
    {"name": "Main", "url": "index"},
    {"name": "Sign-In", "url": "auth"},
    {"name": "About", "url": "about"},
]


def connect_db():
    """
    Obtain database connection
    """
    print_debug(application=app, message="get connection")
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection


def create_db():
    """
    Create database from sql scratch
    """
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as file:
        db.cursor().execute(file.read())
    db.commit()
    db.close()


def get_db():
    """
    Obtain the database connection linked by request global context

    :returns: database connection
    """
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/index')
@app.route('/')
def index():
    """
    Rander main page
    """
    print_debug(application=app, message=url_for('index'))
    print("session key is " + app.config['SECRET_KEY'])
    db = get_db()

    return render_template(
        'index.html',
        title="Main",
        header="Main page",
        menu=[],
    )


@app.route('/auth', methods=["POST", "GET"])
def auth():
    """
    Render login page
    """
    print_debug(application=app, message=url_for('auth'))

    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == "POST" and request.form['login'] == "user" and request.form['password'] == "1234":
        session['userLogged'] = request.form['login']
        return redirect(url_for('profile', username=session['userLogged']))

    if request.method == "POST":
        if not request.form["login"] or not request.form["password"]:
            flash("Нечего отправлять", category='error')
        else:
            flash("Сообщение ушло", category='success')
        print_debug(application=app, message=request.form)

    return render_template(
        'auth.html',
        title="Log-in",
        header="Authorization",
        menu=main_menu,
    )


@app.route('/profile/<username>')
def profile(username):
    """
    Render profile page

    :param username: current username
    """
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Wellcome, {username}"


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
        menu=main_menu,
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
        menu=main_menu,
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
        menu=main_menu,
    ), 401


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4999)
