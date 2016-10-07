# coding=utf-8
from application import db, bcrypt


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.set_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def set_password_hash(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<Admin id=%s username=%s password=%s >' % \
               (self.id, self.username, self.password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Category id=%s title=%s >' % (self.id, self.title)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    picture = db.Column(db.String, default='default')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(
        'Category', backref=db.backref('products', lazy='dynamic'))

    def __init__(self, title, description, price, category_id, picture=None):
        self.title = title
        self.description = description
        self.price = price
        self.category_id = category_id
        self.picture = picture

    def __repr__(self):
        return '<Product id=%s title=%s description=%s price=%s picture=%s ' \
               'category_id=%s >' % (self.id, self.title, self.description,
                                     self.price, self.picture, self.category_id)
