# coding=utf-8
from decimal import Decimal
from flask import abort
from flask import render_template, request, redirect, url_for, session

from application import app
from application.db_helper import convert_to_money_format, \
    convert_to_decimal_format, convert_to_integer
from application.forms import CategoryForm, ProductForm, PriceFilterForm
from application.services import AdminService, CategoryService, ProductService
import logging


log = logging.getLogger(__name__)


@app.route('/')
def get_index_page():
    categories = CategoryService.get_all_categories()
    price_form = PriceFilterForm()
    price_form.from_field.data = None if not session.get('price_from') \
        else convert_to_decimal_format(session.get('price_from'))
    price_form.to_field.data = None if not session.get('price_to') \
        else convert_to_decimal_format(session.get('price_to'))
    return render_template(
        'index.html', is_admin=session.get('is_admin'),
        categories=categories, price_form=price_form)


@app.route('/category/<int:category_id>/page/<int:page>')
def get_products_page(category_id, page):
    price_form = PriceFilterForm()
    price_form.from_field.data = None if not session.get('price_from') \
        else convert_to_decimal_format(session.get('price_from'))
    price_form.to_field.data = None if not session.get('price_to') \
        else convert_to_decimal_format(session.get('price_to'))
    data = ProductService \
        .get_categories_and_products_by_category_id(
            category_id, page, min_price=session.get('price_from', 0),
            max_price=session.get('price_to'))
    return render_template(
        'index.html', is_admin=session.get('is_admin'),
        categories=data['categories'], products=data['products'],
        converter=convert_to_money_format, pages=data['total_pages'],
        current_page=page, price_form=price_form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        login_confirmed = AdminService.check_admin_login(
            request.form['username'], request.form['password'])
        if login_confirmed:
            session['is_admin'] = True
            return redirect(url_for('get_index_page'))
        else:
            error = 'login/password is incorrect'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    del session['is_admin']
    return redirect(url_for('get_index_page'))


@app.route('/edit')
def get_edit_page():
    if not session.get('is_admin'):
        abort(404)
    return render_template('edit.html')


@app.route('/edit/category')
def get_edit_categories_page():
    if not session.get('is_admin'):
        abort(404)
    categories = CategoryService.get_all_categories()
    return render_template('edit_categories.html', categories=categories)


@app.route('/edit/category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    if not session.get('is_admin'):
        abort(404)

    form = CategoryForm()
    error = None
    if request.method == 'POST':
        form = CategoryForm(request.form)
        if 'update' in request.form:
            if form.validate():
                success = CategoryService \
                    .update_category_by_id(category_id, form.title.data)
                if success:
                    return redirect(url_for('get_categories_page'))
        else:
            error = CategoryService.delete_category_by_id(category_id)
            if not error:
                return redirect(url_for('get_categories_page'))
    else:
        category = CategoryService.get_category_by_id(category_id)
        if not category:
            abort(404)
        form.title.data = category.title

    return render_template('edit_category.html', form=form, error=error)


@app.route('/edit/category/new', methods=['GET', 'POST'])
def new_category():
    if not session.get('is_admin'):
        abort(404)

    form = CategoryForm()
    error = None
    if request.method == 'POST':
        form = CategoryForm(request.form)
        if form.validate():
            error = CategoryService.create_new_category(form.title.data)
            if not error:
                return redirect(url_for('get_categories_page'))
    return render_template('edit_new_category.html', form=form, error=error)


@app.route('/edit/product')
def get_edit_products_page():
    if not session.get('is_admin'):
        abort(404)
    products = ProductService.get_all_products()
    return render_template('edit_products.html', products=products,
                           converter=convert_to_money_format)


@app.route('/edit/product/new', methods=['GET', 'POST'])
def new_product():
    if not session.get('is_admin'):
        abort(404)
    form = ProductForm()
    error = None
    if request.method == 'POST':
        form = ProductForm(request.form)
        if form.validate():
            error = ProductService.create_new_product({
                'title': form.title.data,
                'price': form.price.data,
                'description': form.description.data,
                'category_id': request.form.get('category_id')
            })
            if not error:
                return redirect(url_for('get_edit_products_page'))
    categories = CategoryService.get_all_categories()
    return render_template('edit_new_product.html', form=form,
                           categories=categories, error=error)


@app.route('/edit/product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if not session.get('is_admin'):
        abort(404)
    form = ProductForm()
    error = None
    categories, product = \
        ProductService.get_categories_and_product_by_product_id(product_id)
    if not product:
        abort(404)
    if request.method == 'POST':
        if 'update' in request.form:
            form = ProductForm(request.form)
            if form.validate():
                error = ProductService.update_product_by_product_id(
                    product_id,
                    {
                        'title': form.title.data,
                        'description': form.description.data,
                        'price': form.price.data,
                        'category_id':
                            request.form[
                                'category_id']
                    })
                if not error:
                    return redirect(url_for('get_edit_products_page'))
        else:
            error = ProductService.delete_product_by_id(product_id)
            if not error:
                return redirect(url_for('get_edit_products_page'))
    else:
        form.title.data = product.title
        form.description.data = product.description
        form.price.data = convert_to_decimal_format(product.price)
    return render_template('edit_product.html', form=form, product=product,
                           categories=categories, error=error)


@app.route('/price-filter', methods=['POST'])
def post_price_filter():
    if 'delete' in request.form:
        del session['price_from']
        del session['price_to']
        log.info('Price filter was cleared')
    else:
        try:
            form = PriceFilterForm()
            form.from_field.data = convert_to_integer(Decimal(request.form.get('from_field'))) \
                if request.form.get('from_field') != u'' else 0
            form.to_field.data = convert_to_integer(Decimal(request.form.get('to_field'))) \
                if request.form.get('to_field') != u'' \
                else ProductService.fetch_max_price()
            if form.validate():
                session['price_to'] = form.to_field.data
                session['price_from'] = form.to_field.data \
                    if form.to_field.data < form.from_field.data \
                    else form.from_field.data
                log.info('Price filter was set from %s to %s' \
                         % (request.form.get('from_field'),
                            request.form.get('to_field')))
        except ValueError:
            log.error('Error occurred while set price filter from %s to %s' \
                      % (request.form.get('from_field'),
                         request.form.get('to_field')))
    return redirect(url_for('get_index_page'))
