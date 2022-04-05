from flask_sqlalchemy import Pagination
from sqlalchemy.orm.session import close_all_sessions
from app.wiki import blueprint
from flask import render_template, redirect, url_for, request, make_response, jsonify, json, flash
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from ..base.models import Case,User,UserRole,Version,Wiki,default_pass,role_check
from .. import db
from app.base.util import up_version,get_ver_lg
from datetime import datetime
from .. import tasks

@blueprint.route('/wiki', methods=['GET','POST'])
@login_required
def wiki():
    page = request.args.get('page_wiki', 1, type=int)
    pagination = Wiki.query.order_by(Wiki.timestamp.desc()).paginate(
        page, per_page=10, error_out=False)
    wikis = pagination.items
    return render_template('wiki.html', wikis=wikis, pagoination=pagination, segment='wiki')

@blueprint.route('/wiki_editor', methods=['GET','POST'])
@login_required
def wiki_editor():
    print("wikiwikiwiki")
    return render_template('wiki-editor.html')