#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from flask import Flask, render_template, url_for, request, flash


app = Flask(__name__)
app.config["SECRET_KEY"] = f"{uuid.uuid1()}"

main_menu = [
    {"name": "Sign-In", "url": "index"},
    {"name": "About", "url": "about"},
]


@app.route('/index')
@app.route('/auth', methods=["POST"])
@app.route('/')
def index():
    """
    rander main page
    """
    # debug logging
    print(url_for('index'))
    print("session key is " + app.config['SECRET_KEY'])

    if request.method == "POST":
        if not request.form["login"] or not request.form["password"]:
            flash("Нечего отправлять", category='error')
        else:
            flash("Сообщение ушло", category='success')
        print(request.form)

    return render_template(
        'index.html',
        title="Log-in",
        header="Authorization",
        menu=main_menu,
    )


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
    render error page
    """
    # debug logging
    print(error)
    return render_template(
        'pageNotFound.html',
        title="Page not found",
        header="Error",
        menu=main_menu,
    ), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4999)
