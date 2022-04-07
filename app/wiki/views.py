from flask_sqlalchemy import Pagination
from sqlalchemy.orm.session import close_all_sessions
from app.wiki import blueprint
from flask import render_template, redirect, url_for, request, make_response, jsonify, json, flash
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from ..base.models import Wiki
from .. import db
from app.base.util import up_version,get_ver_lg
from datetime import datetime
from .. import tasks
import time
from os import path

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
    return render_template('wiki-editor.html')

@blueprint.route('/save', methods=['GET','POST'])
@login_required
def save():
    title = request.form['title']
    content = request.form['content'].replace('\n','')
    credate = datetime.now().strftime('%Y-%m-%d')
    filename = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    filepath = f'app/wiki/static/md/{filename}_{title}.md'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        f.close()
    print(current_user,current_user._get_current_object)
    new_wiki = Wiki(author=current_user._get_current_object(),title=title,content=f'{filename}_{title}.md')
    db.session.add(new_wiki)
    db.session.commit()

    return redirect("/wiki")


@blueprint.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    file = request.files.get('editormd-image-file')
    if not file:
        res = {
            'success' : 0,
            'message' : '上传失败'
        }
    else:
        pass

@blueprint.route('/wiki-view/<int:wiki_id>', methods=['GET','POST'])
@login_required
def wiki_view(wiki_id):
    wiki = Wiki.query.get_or_404(wiki_id)


