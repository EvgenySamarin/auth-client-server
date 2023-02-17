#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from flask.app import Flask
from flask.helpers import url_for, redirect, flash, abort
from flask.globals import session, request
from flask.templating import render_template


app = Flask(__name__)
app.config["SECRET_KEY"] = f"{uuid.uuid1()}"


main_menu = [
    {"name": "Main", "url": "index"},
    {"name": "Sign-In", "url": "auth"},
    {"name": "About", "url": "about"},
]


@app.route('/index')
@app.route('/')
def index():
    """
    rander main page
    """
    # debug logging
    print(url_for('index'))
    print("session key is " + app.config['SECRET_KEY'])

    return render_template(
        'index.html',
        title="Main",
        header="Main page",
        menu=main_menu,
    )


@app.route('/auth', methods=["POST", "GET"])
def auth():
    """
    render login page
    """
    # debug logging
    print(url_for('auth'))

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
        print(request.form)

    return render_template(
        'auth.html',
        title="Log-in",
        header="Authorization",
        menu=main_menu,
    )


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Wellcome, {username}"


@app.route('/about')
def about():
    """
    render about page
    """
    # debug logging
    print(url_for('about'))
    return render_template(
        'about.html',
        title="About us",
        header="About site",
        menu=main_menu,
    )


@app.errorhandler(404)
def page_not_found(error):
    """
    render error page not found
    """
    # debug logging
    print(error)
    return render_template(
        'error.html',
        title="Page not found",
        header="Error",
        menu=main_menu,
    ), 404


@app.errorhandler(401)
def page_not_found(error):
    """
    render error page unauthorized
    """
    # debug logging
    print(error)
    return render_template(
        'error.html',
        title="Page not found",
        header="Unauthorized",
        menu=main_menu,
    ), 401


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4999)