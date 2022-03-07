from flask_login import UserMixin
from sqlalchemy import BINARY, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app import db, login_manager

from app.base.util import hash_pass

default_pass = hash_pass("123456")

class EntityBase(object):
    def to_json(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]       
        return fields

class Permission:
    COMMIT = 0x01
    FINISH = 0x02
    ADMINISTRATOR = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permission = db.Column(db.Integer)
    user = db.relationship('User', backref='role', lazy='dynamic')

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
    role_id = Column(String, ForeignKey('roles.role_id'))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = hash_pass( value )

            setattr(self, property, value)

    @staticmethod
    def create_superadmin():
        users = {
            'gz0645': (hash_pass('112358'),3)
        }
        for u in users:
            user = User.query.filter_by(username=u).first()
            if user is None:
                user = User(username=u)
            user.password = users[u][0]
            user.role_id = users[u][1]
            db.session.add(user)
        db.session.commit()

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