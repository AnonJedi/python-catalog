# coding=utf-8
from decimal import Decimal
from flask import g
from application import app, db


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = db.session
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.commit()
        g.sqlite_db.close()


def convert_to_integer(decimal_number):
    """
    Convert number from money format like '18.50' to integer '1850'
    """
    return int(decimal_number) * 100


def convert_to_money_format(integer_number):
    """
    Convert number from integer like '1850' to money format '18.50'
    """
    return u'%s р' % (Decimal(integer_number) / 100)


def convert_to_decimal_format(integer_number):
    return Decimal(integer_number) / 100
