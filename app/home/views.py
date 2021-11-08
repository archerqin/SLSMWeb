from app.home import blueprint
from flask import render_template, redirect, url_for, request, make_response
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from ..base.models import Bug

@blueprint.route('/index')
@login_required
def index():
    return render_template('index.html', segment='index')


@blueprint.route('/bug/flag=<int:flag>')
def show_bugs(flag):
    if flag == 1:
        resp = make_response(redirect(url_for('.index')))
        print("show_bugs flag1")
        return resp

@blueprint.route('/caseSubmit', method=['Get', 'Post'])
def case_submit():
    pass
    