# coding=utf-8
from flask import Flask, session, abort
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)
app.secret_key = 'store test secret key'


@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or unicode(token) != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = random.getrandbits(128)
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from application.controllers import *
from application.models import *
