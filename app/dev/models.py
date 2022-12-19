from flask_login import UserMixin
from sqlalchemy import BINARY, BLOB, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
import time
import json

from app import db,login_manager
# from ../..

class System(db.Model):
    __tablename__ = 'systems'
    id = db.Column(db.Integer, primary_key=True)


class Dev(db.Model):
    __tablename__ = 'devs'
    id = db.Column(db.Integer, primary_key=True)
    # type = 
    title = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())



##system
##function
##adjust
##bug


##相当于bug
##id
##text
##images
class Fix(db.Model):
    __tablename__ = 'fixs'
    id = db.Column(db.Integer, primary_key=True)

