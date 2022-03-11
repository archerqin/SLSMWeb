from flask_login import UserMixin
from sqlalchemy import BINARY, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
import json

from app import db, login_manager

from app.base.util import hash_pass

default_pass = hash_pass("123456")
super_admins = {
            'gz0645': ('112358','秦浩翔','[1,2,7]')
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
    username = Column(String, unique=True)
    name = Column(String, unique=True)
    password = Column(BINARY)
    userroles = db.relationship('UserRole',
                            foreign_keys=[UserRole.user_id],
                            backref='user',
                            lazy='dynamic')

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
            print(UserRole.query.filter_by(user_id=user.id))

            if user is None:
                user = User(username=u, password=super_admins[u][0], name=super_admins[u][1])
                for r_id in rolelist:
                    role = Role.query.filter_by(role_id=r_id).first()
                    UserRole.set_userrole(user.id, role.id)
            ##相当于可以重置除username外的其他信息
            ##如果发现配置角色中没有某个职位，则删除
            else:
                # user = User(password=super_admins[u][0], name=super_admins[u][1])
                oldRoleList =[ur.role_id for ur in UserRole.query.filter_by(user_id=user.id)]
                print(oldRoleList)
                for oldr in oldRoleList:
                    if oldr not in rolelist:
                        UserRole.unset_userrole(user.id, oldr)
                for r_id in rolelist:
                    UserRole.set_userrole(user.id, r_id)

            db.session.add(user)
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
    region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'))
    state = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.Integer, index=True, default=int(datetime.timestamp(datetime.now())))

##版本号-->case_id 一对多
class Version(db.Model): 
    __tablename__ = 'versions'
    version_id = db.Column(db.Integer, primary_key=True)
    version_name = db.Column(db.String(32))
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
class Region(db.Model):  
    __tablename__ = 'regions'
    region_id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(32))