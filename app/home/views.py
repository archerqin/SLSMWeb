from flask_sqlalchemy import Pagination
from sqlalchemy.orm.session import close_all_sessions
from app.home import blueprint
from flask import render_template, redirect, url_for, request, make_response, jsonify, json, flash
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from ..base.models import Case
from .. import db
import time

@blueprint.route('/index', methods=['GET','POST'])
@login_required
def index():
    # cases = Case.query.all()
    query = Case.query
    # for case in cases:
    #     print(case)

    page = request.args.get('page', 1, type=int)
    print("index:",page)
    pagination = query.order_by(Case.timestamp.desc()).paginate(
        page, per_page=5, error_out=False)
    cases = pagination.items

    return render_template('index.html', cases=cases, pagination=pagination)

@blueprint.route('/case/flag=<int:flag>')
def show_cases(flag):
    if flag == 1:
        resp = make_response(redirect(url_for('.index')))
        print("show_cases flag1")
        return resp

@blueprint.route('/case_commit', methods=['GET', 'POST'])
def case_commit():
    print("case_commit")
    # resp = make_response(redirect(url_for('.index')))
    # return resp
    data = json.loads(request.form.get('data'))
    text = data['text']
    desc = data['desc']
    timestamp = int(time.time())
    print(text, desc)
    case = Case(text=text, detail=desc, timestamp=timestamp)
    db.session.add(case)
    db.session.commit()
    return redirect(url_for('.index'))
    # return render_template('index.html',data=data)

@blueprint.route('/case_delete', methods=['GET', 'POST'])
def case_delete():
    data = json.loads(request.form.get('data'))
    case_id = data['id']
    case = Case.query.get_or_404(case_id)
    db.session.delete(case)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        flash('删除失败！')
    else:
        flash('删除成功')
    page = request.args.get('page', 1, type=int)

    return redirect(url_for('.index', case_id=case.case_id, page=page))

@blueprint.route('/autotest')
@login_required
def autotest():
    return render_template('autotest.html', segment='autotest')

@blueprint.route('/testcase')
@login_required
def testcase():
    return render_template('testcase.html', segment='testcase')