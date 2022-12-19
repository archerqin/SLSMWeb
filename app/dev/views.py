from flask_sqlalchemy import Pagination
from sqlalchemy.orm.session import close_all_sessions
from app.dev.models import Dev
from app.wiki import blueprint
from flask import render_template, redirect, url_for, request, make_response, jsonify, json, flash, Response
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from .. import db
from app.base.util import up_version,get_ver_lg
from datetime import datetime
# from ... import tasks
import time
from os import path


@blueprint.route('/dev', methods=['GET','POST'])
@login_required
def dev():
    page = request.args.get('page_dev', 1, type=int)
    pagination = Dev.query.order_by(Dev.timestamp.desc()).paginate(
        page, per_page=15, error_out=False)
    devs = pagination.items
    return render_template('dev.html', devs=devs, pagination=pagination, segment='dev')