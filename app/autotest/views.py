from flask_sqlalchemy import Pagination
from sqlalchemy.orm.session import close_all_sessions
from app.autotest import blueprint
from flask import render_template, redirect, url_for, request, make_response, jsonify, json, flash, Response
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from ..base.models import AutoTest
from .. import db
from app.base.util import up_version,get_ver_lg
from datetime import datetime
# from ... import tasks
import time
from os import path

@blueprint.route('/autotest', methods=['GET','POST'])
@login_required
def wiki():
    page = request.args.get('page_autotest', 1, type=int)
    print(page)
    pagination = AutoTest.query.order_by(AutoTest.timestamp.desc()).paginate(
        page, per_page=15, error_out=False)
    autotests = pagination.items
    return render_template('autotest.html', autotests=autotests, pagination=pagination, segment='autotest')