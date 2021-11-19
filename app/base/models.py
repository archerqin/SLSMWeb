from flask_login import UserMixin
from sqlalchemy import BINARY, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app import db, login_manager

from app.base.util import hash_pass

class Permission:
    COMMITBUG = 0x01
    FINISHBUGS = 0x02
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
            'User':(Permission.COMMITBUG |
                    Permission.FINISHBUGS, True),
            'Administrator':(0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permission = roles[r][0]
            db.session.add(role)
        db.session.commit()
    
    def _repr__(self):
        return '<Role %r>' % self.name

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(BINARY)
    role_id = Column(String, ForeignKey('roles.role_id'))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = hash_pass( value )

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    
@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None


class Bug(db.Model):
    __tablename__ = 'bugs'
    bug_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    detail = db.Column(db.Text, default="")
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    maintainer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    version_id = db.Column(db.Integer, db.ForeignKey('versions.version_id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'))
    state = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.Integer, index=True, default=int(datetime.timestamp(datetime.now())))

class Version(db.Model):
    __tablename__ = 'versions'
    version_id = db.Column(db.Integer, primary_key=True)
    version_name = db.Column(db.String(32))
    
class Class(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(32))

class Region(db.Model):
    __tablename__ = 'regions'
    region_id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(32))