# coding=utf-8
from wtforms import StringField, validators, DecimalField, IntegerField
from wtforms.form import Form


class CategoryForm(Form):
    title = StringField(u'Title', validators=[validators.input_required()])


class ProductForm(Form):
    title = StringField(u'Title', validators=[validators.input_required()])
    price = DecimalField(
        u'Price', validators=[validators.input_required()])
    description = StringField(u'Description',
                              validators=[validators.input_required()])
