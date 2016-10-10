# coding=utf-8
from wtforms import StringField, validators, DecimalField, TextAreaField
from wtforms.form import Form


class CategoryForm(Form):
    title = StringField(u'Title', validators=[validators.input_required()])


class ProductForm(Form):
    title = StringField(u'Title', validators=[validators.input_required()])
    price = DecimalField(
        u'Price', validators=[validators.input_required()])
    description = TextAreaField(u'Description',
                                validators=[validators.input_required()])


class PriceFilterForm(Form):
    from_field = DecimalField(u'From')
    to_field = DecimalField(u'To')
