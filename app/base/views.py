from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User

from app.base.util import verity_pass

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and verity_pass( password, user.password):

            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        return render_template( 'accounts/login.html',
                                msg='错误的用户名或密码',
                                form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']

        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html',
                                    msg='',
                                    success=False,
                                    form=create_account_form)

        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template( 'accounts/register.html',
                                msg='用户创建,请<a href="/login">登录</a>',
                                success=True,
                                form=create_account_form)

    else:
        return render_template( 'accounts/register.html', 
                                form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500

