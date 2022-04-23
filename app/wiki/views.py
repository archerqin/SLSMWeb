from flask_sqlalchemy import Pagination
from sqlalchemy.orm.session import close_all_sessions
from app.wiki import blueprint
from flask import render_template, redirect, url_for, request, make_response, jsonify, json, flash, Response
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
    print(page)
    pagination = Wiki.query.order_by(Wiki.timestamp.desc()).paginate(
        page, per_page=15, error_out=False)
    wikis = pagination.items
    return render_template('wiki.html', wikis=wikis, pagination=pagination, segment='wiki')

@blueprint.route('/wiki_editor', methods=['GET','POST'])
@login_required
def wiki_editor():
    return render_template('wiki-editor.html')

@blueprint.route('/wiki_reedit/<int:wiki_id>', methods=['GET','POST'])
@login_required
def wiki_reedit(wiki_id):
    wiki = Wiki.query.get_or_404(wiki_id)
    filepath = 'app/wiki/static/md/'+wiki.content
    with open(filepath) as f:
        content = f.read()
        f.close()
    return render_template('wiki-reedit.html',wiki=wiki,content=content)

@blueprint.route('/save/<int:wiki_id>', methods=['GET','POST'])
@login_required
def save(wiki_id):
    if wiki_id == 0:
        title = request.form['title']
        content = request.form['content'].replace('\n','')
        credate = datetime.now().strftime('%Y-%m-%d')
        filename = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        filepath = f'app/wiki/static/md/{filename}_{title}.md'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            f.close()
        new_wiki = Wiki(author=current_user._get_current_object(),title=title,content=f'{filename}_{title}.md')
        db.session.add(new_wiki)
    else:
        print(wiki_id)
        wiki = Wiki.query.get_or_404(wiki_id)
        title = request.form['title']
        content = request.form['content'].replace('\n','')
        filepath = f'app/wiki/static/md/{wiki.content}'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            f.close()
        wiki.title = title
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
        ex = path.splitext(file.filename)[1]
        print(ex)
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
        print(filename)
        file.save(f'app/wiki/static/upload/%s' % filename)
        res = {
            'success' : 1,
            'message' : '上传成功',
            'url' : url_for('wiki_blueprint.image', name = filename)
        }
    return jsonify(res)

@blueprint.route('/image/<name>', methods=['GET','POST'])
@login_required
def image(name):
    with open(path.join('app/wiki/static/upload', name), 'rb') as f:
        resp = Response(f.read(), mimetype="image/jpeg")
    return resp

@blueprint.route('/wiki-view/<int:wiki_id>', methods=['GET','POST'])
@login_required
def wiki_view(wiki_id):
    wiki = Wiki.query.get_or_404(wiki_id)
    filepath = 'app/wiki/static/md/'+wiki.content
    with open(filepath) as f:
        content = f.read()
        f.close()
    return render_template('wiki-view.html', wiki=wiki, content=content)

@blueprint.route('/wiki-delete/<int:wiki_id>', methods=['GET','POST'])
@login_required
def wiki_delete(wiki_id):
    wiki = Wiki.query.get_or_404(wiki_id)
    db.session.delete(wiki)
    db.session.commit()
    return redirect("/wiki")
