from email.policy import default
from flask_login import UserMixin
from sqlalchemy import BINARY, BLOB, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
import time
import json

from app import db, login_manager

from app.base.util import hash_pass

default_pass = "123456"
super_admins = {
            'gz0645': ('112358','秦浩翔','[1,2,7]')
        }
role_check = {
    1: 2,  ##超级管理员
    2: 4,  ##管理员
    3: 5,  ##普通
    4: 6,  ##策划
    5: 7,
    6: 8,
    7: 9,
}

class Permission:
    COMMIT = 0x01
    FINISH = 0x02
    ADMINISTRATOR = 0x80

class UserRole(db.Model):
    __tablename__ = 'userroles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    role_id = db.Column(db.Integer, ForeignKey('roles.role_id'))
    
    @staticmethod
    def set_userrole(uid,rid):
        ur = UserRole(user_id=uid, role_id=rid)
        db.session.add(ur)
        db.session.commit()
    @staticmethod
    def unset_userrole(uid,rid):
        ur = UserRole.query.filter_by(user_id=uid, role_id=rid).first()
        db.session.delete(ur)
        db.session.commit()


class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permission = db.Column(db.Integer)
    userroles = db.relationship('UserRole',
                            foreign_keys=[UserRole.role_id],
                            backref='role',
                            lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'SuperAdmin':(0xff, False),
            'Administrator':(0xff, False),
            'User':(Permission.COMMIT |
                    Permission.FINISH, True),            
            '策划':(Permission.COMMIT |
                    Permission.FINISH, True),
            '前端':(Permission.COMMIT |
                    Permission.FINISH, True),
            '后端':(Permission.COMMIT |
                    Permission.FINISH, True),
            '测试':(Permission.COMMIT |
                    Permission.FINISH, True),
            '运营':(Permission.COMMIT |
                    Permission.FINISH, True),
            '美术':(Permission.COMMIT |
                    Permission.FINISH, True)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permission = roles[r][0]
            print(role)
            db.session.add(role)
        db.session.commit()
    
    

    def _repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    name = Column(String(32), unique=True)
    password = Column(BLOB)
    userroles = db.relationship('UserRole',
                            foreign_keys=[UserRole.user_id],
                            backref='user',
                            lazy='dynamic')
    wikis = db.relationship('Wiki', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = hash_pass( value )

            setattr(self, property, value)

    # def do_user_has_role(self, role):
    #     return self.userroles.filter_by(role_id=role.id).first() is not None

    @staticmethod
    def create_superadmin():
        for u in super_admins:
            user = User.query.filter_by(username=u).first()
            rolelist = json.loads(super_admins[u][2])
            # print(UserRole.query.filter_by(user_id=user.id))

            if user is None:
                user = User(username=u, password=super_admins[u][0], name=super_admins[u][1])
                
            ##相当于可以重置除username外的其他信息
            ##如果发现配置角色中没有某个职位，则删除
            else:
                # user = User(password=super_admins[u][0], name=super_admins[u][1])
                oldRoleList =[ur.role_id for ur in UserRole.query.filter_by(user_id=user.id)]
                print(oldRoleList)
                for oldr in oldRoleList:
                    if oldr not in rolelist:
                        UserRole.unset_userrole(user.id, oldr)

            db.session.add(user)
            for r_id in rolelist:
                role = Role.query.filter_by(role_id=r_id).first()
                print(user.id)
                UserRole.set_userrole(user.id, role.role_id)
        db.session.commit()

    def get_role(self, user):
        s = self.userroles.filter_by(user_id=user.id)
        print(s)

    def __repr__(self):
        # return str(self.username)
        return '<User %r>' % self.username

    
@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

##项目
class Project(db.Model):
    __tablename__ = 'projects'
    proj_id = db.Column(db.Integer, primary_key=True)
    proj_name = db.Column(String(32), unique=True)
    proj_alias = db.Column(String(32), unique=True)
    lang_name = db.Column(String(32))
    lang_alias = db.Column(String(32))
    cases = db.relationship('Case',
                            backref = 'projcases',
                            lazy = 'dynamic')
    versions = db.relationship('Version',
                            backref = 'projversions',
                            lazy = 'dynamic')
    wikis = db.relationship('Wiki',
                            backref = 'projwikis',
                            lazy = 'dynamic')

    def __repr__(self):
        return '<Project %r>' % self.proj_alias+self.lang_alias


# class Lang(db.Model):
#     __tablename__ = 'langs'
#     lang_id = db.Column(db.Integer, primary_key=True)
#     lang_abbr = db.Column(db.String(32),default="CN")
#     lang_name = db.Column(db.String(32),default="中国大陆")

##修改case
class Case(db.Model):  
    __tablename__ = 'cases'
    case_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, default=1)
    text = db.Column(db.Text)
    detail = db.Column(db.Text, default="")
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    maintainer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    version_id = db.Column(db.Integer, db.ForeignKey('versions.version_id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    proj_id = db.Column(db.Integer, db.ForeignKey('projects.proj_id'))
    state = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    
    @staticmethod
    def drop_cases():
        cases = Case.query.all()
        for case in cases:
            db.session.delete(case)


##版本号-->case_id 一对多
class Version(db.Model): 
    __tablename__ = 'versions'
    version_id = db.Column(db.Integer, primary_key=True)
    version_name = db.Column(db.String(32))
    desc = db.Column(db.Text, default="")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    cases = db.relationship('Case',
                            backref = 'cases',
                            lazy = 'dynamic')
    @staticmethod
    def versionCase():
        pass

##
class Class(db.Model):  
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(32))

##地区
# class Region(db.Model):  
#     __tablename__ = 'regions'
#     region_id = db.Column(db.Integer, primary_key=True)
#     region_name = db.Column(db.String(32))

##wiki
class Wiki(db.Model):
    __tablename__ = 'wikis'
    wiki_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(64))
    content = db.Column(db.Text, default="")
    publish = db.Column(db.Integer, default=0)  #默认未发布
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
