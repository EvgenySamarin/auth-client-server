#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

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

    if request.method == "POST":
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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4999)
