from flask import render_template, request, redirect, url_for, session

from application import app
from application.services import AdminService


@app.route('/')
def get_index_page():
    return render_template('index.html', is_admin=session.get('is_admin'))


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
