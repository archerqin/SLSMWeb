from sqlalchemy.orm.session import close_all_sessions
from app.home import blueprint
from flask import render_template, redirect, url_for, request, make_response, jsonify, json
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from ..base.models import Bug
from .. import db

@blueprint.route('/index')
@login_required
def index():
    cases = Bug.query.all()
    # for case in cases:
    #     print(case)


    return render_template('index.html', segment='index', cases=cases)

@blueprint.route('/bug/flag=<int:flag>')
def show_bugs(flag):
    if flag == 1:
        resp = make_response(redirect(url_for('.index')))
        print("show_bugs flag1")
        return resp

@blueprint.route('/case_commit', methods=['Get', 'Post'])
def case_commit():
    print("case_commit")
    # resp = make_response(redirect(url_for('.index')))
    # return resp
    data = json.loads(request.form.get('data'))
    text = data['text']
    desc = data['desc']
    print(text, desc)
    case = Bug(text=text, detail=desc)
    db.session.add(case)
    db.session.commit()
    return jsonify(data)

@blueprint.route('/testcase')
@login_required
def testcase():
    return render_template('testcase.html', segment='testcase')