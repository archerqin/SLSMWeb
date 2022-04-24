from crypt import methods
from tkinter import PROJECTING
from flask_sqlalchemy import Pagination
from sqlalchemy.orm.session import close_all_sessions
from app.home import blueprint
from flask import render_template, redirect, url_for, request, make_response, jsonify, json, flash
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from ..base.models import Case,User,UserRole,Version,Project,default_pass,role_check
from .. import db
from app.base.util import up_version,get_ver_lg
from datetime import datetime
from .. import tasks

@blueprint.route('/index', methods=['GET','POST'])
@login_required
def index():
    proj = Project.query.first()
    request.args.get('proj', proj.proj_id, type=int)
    versions = Version.query.order_by(Version.timestamp.desc()).limit(3).all()
    return render_template('version-overview.html', versions=versions, segment='index')

@blueprint.route('/case_online', methods=['GET','POST'])
@login_required
def case_online():
    page = request.args.get('page', 1, type=int)
    # case_type = 1
    if current_user.is_authenticated:
        case_type = int(request.cookies.get('case_type', '') or 1)
    query = Case.query.filter(Case.type_id == case_type)

    pagination = query.order_by(Case.timestamp.desc()).paginate(
        page, per_page=5, error_out=False)
    cases = pagination.items
    return render_template('case-online.html', cases=cases, pagination=pagination, case_type=case_type, segment='case_online')

@blueprint.route('/case1') ##bug
def case_1():
    resp = make_response(redirect(url_for('.case_online')))
    resp.set_cookie('case_type', '1', max_age=30*24*60*60)
    return resp

@blueprint.route('/case2') ##策划修改
def case_2():
    resp = make_response(redirect(url_for('.case_online')))
    resp.set_cookie('case_type', '2', max_age=30*24*60*60)
    return resp

@blueprint.route('/case3') ##程序优化
def case_3():
    resp = make_response(redirect(url_for('.case_online')))
    resp.set_cookie('case_type', '3', max_age=30*24*60*60)
    return resp

@blueprint.route('/case_commit', methods=['GET', 'POST'])
def case_commit():##可以把edit也写在这里，判断有没有id
    print("case_commit")
    # resp = make_response(redirect(url_for('.index')))
    # return resp
    data = json.loads(request.form.get('data'))
    print(data)
    text = data['text']
    desc = data['desc']
    type = data['type']
    ver = data['ver']
    print(ver)
    # timestamp = int(time.time())
    case = Case(type_id=type, text=text, detail=desc, version_id=ver)
    db.session.add(case)
    db.session.commit()
    return redirect(url_for('.case_online'))
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

    return redirect(url_for('.case_online', case_id=case.case_id, page=page))

@blueprint.route('/set_case_info', methods=['GET', 'POST'])
def set_case_info():
    data = json.loads(request.form.get('data'))
    case_id = data['case_id']
    case = Case.query.get_or_404(case_id)
    caseinfo = {"case_id":case.case_id,
                "text":case.text,
                "detail":case.detail,
                }
    return jsonify(caseinfo)


@blueprint.route('/autotest')
@login_required
def autotest():
    return render_template('autotest.html', segment='autotest')

@blueprint.route('/testcase')
@login_required
def testcase():
    return render_template('testcase.html', segment='testcase')


@blueprint.route('/settings')
@login_required
def settings():
    return render_template('settings.html', segment='settings')

@blueprint.route('/add_user',methods=['GET', 'POST'])
@login_required
def add_user():
    data = json.loads(request.form.get('data'))
    username = data['username']
    realname = data['name']
    rolechecks = data['rolechecks']
    user = User.query.filter_by(username=username).first()
    print(user,rolechecks)
    if user is None:
        user = User(username=username,name=realname,password=default_pass)
    else:
        print("已存在该帐号")
        flash("已存在该帐号")
    db.session.add(user)
    db.session.commit()
    for rc in rolechecks:
        UserRole.set_userrole(user.id, role_check[rc])
    users=User.query.all()
    allusers = []
    if users:
        for u in users:
            u1 = {}
            u1["username"] = u.username
            u1["name"] = u.name
            uroles = []
            for ur in u.userroles:
                uroles.append(ur.role_id)
            u1["uroles"] = uroles
            allusers.append(u1)
    return jsonify(allusers)

@blueprint.route('/get_users',methods=['GET', 'POST'])
@login_required
def get_users():
    users=User.query.all()
    allusers = []
    if users:
        for u in users:
            u1 = {}
            u1["username"] = u.username
            u1["name"] = u.name
            uroles = []
            for ur in u.userroles:
                uroles.append(ur.role_id)
            u1["uroles"] = uroles
            allusers.append(u1)
    return jsonify(allusers)

@blueprint.route('/get_versions',methods=['GET', 'POST'])
@login_required
def get_versions():
    versions=Version.query.order_by(Version.version_id.desc()).limit(10).all()
    allvers = []
    if versions:
        for ver in versions:
            v = {}
            v["verid"] = ver.version_id
            v["verlg"] = get_ver_lg(ver.version_name)
            v["vername"] = ver.version_name
            v["verdesc"] = ver.desc
            v["timestamp"] = ver.timestamp.strftime('%g-%m-%d')
            allvers.append(v)
    
    return jsonify(allvers)

@blueprint.route('/gen_version/<int:typeID>',methods=['GET', 'POST'])
@login_required
def gen_version(typeID):
    last_version=Version.query.order_by(Version.version_id.desc()).first()
    print(last_version)
    if last_version:
        new_version = up_version(last_version.version_name,typeID)
    else:
        new_version="1.0.0.000"

    return new_version

@blueprint.route('/add_version',methods=['GET', 'POST'])
@login_required
def add_version():
    data = json.loads(request.form.get('data'))
    vername = data['vername']
    verdesc = data['verdesc']
    new_version = Version(version_name=vername, desc=verdesc)
    db.session.add(new_version)
    db.session.commit()

    versions=Version.query.order_by(Version.version_id.desc()).limit(10).all()
    allvers = []
    if versions:
        for ver in versions:
            v = {}
            v["verid"] = ver.version_id
            v["verlg"] = get_ver_lg(ver.version_name)
            v["vername"] = ver.version_name
            v["verdesc"] = ver.desc
            v["timestamp"] = ver.timestamp.strftime('%g-%m-%d')
            allvers.append(v)
    
    return jsonify(allvers)

@blueprint.route('/get_verdesc/<int:verID>',methods=['GET', 'POST'])
@login_required
def get_verdesc(verID):
    ver = Version.query.get_or_404(verID)
    verinfo = {}
    verinfo["vername"] = ver.version_name
    verinfo["verdesc"] = ver.desc or ""
    return verinfo

def all_proj():
    projects=Project.query.order_by(Project.proj_id.desc()).all()
    allprojs = []
    print(projects)
    if projects:
        for proj in projects:
            p = {}
            p["projid"] = proj.proj_id
            p["projname"] = proj.proj_name
            p["projalias"] = proj.proj_alias
            p["langname"] = proj.lang_name
            p["langalias"] = proj.lang_alias
            allprojs.append(p)
    
    return allprojs

@blueprint.route('/get_projects', methods=['GET', 'POST'])
@login_required
def get_projects():
    projInfo = jsonify(all_proj())
    return projInfo

@blueprint.route('/add_project/<int:proj_id>', methods=['GET', 'POST'])
@login_required
def add_project(proj_id):
    data = json.loads(request.form.get('data'))
    projname = data['projname']
    projalias = data['projalias']
    langname = data['langname']
    langalias = data['langalias']
    if proj_id == 0:
        new_project = Project(proj_name=projname, proj_alias=projalias,
                        lang_name=langname, lang_alias=langalias)
        db.session.add(new_project)
    else:
        proj = Project.query.get_or_404(proj_id)
        proj.proj_name = projname,
        proj.proj_alias=projalias,
        proj.lang_name=langname,
        proj.lang_alias=langalias
        db.session.add(proj)
    db.session.commit()

    projInfo = all_proj()
    return projInfo

@blueprint.route('/edit_project/<int:proj_id>', methods=['GET', 'POST'])
@login_required
def edit_project(proj_id):
    proj = Project.query.get_or_404(proj_id)
    p = {}
    p['projname'] = proj.proj_name
    p['projalias'] = proj.proj_alias
    p['langname'] = proj.lang_name
    p['langalias'] = proj.lang_alias
    return jsonify(p)
