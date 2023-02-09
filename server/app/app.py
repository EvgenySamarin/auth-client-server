#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return "<h1>Hello, World!</h1>"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4999)
