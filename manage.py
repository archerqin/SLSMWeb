import os
from app import create_app, db, celery_config
from app.base.models import *
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from celery import Celery
from config import config_dict
import pymysql
# pymysql.install_as_MySQLdb

def make_celery(app_name):
    celery = Celery(app_name,
                    broker=celery_config.broker_url,
                    backend=celery_config.result_backend)
    
    return celery

my_celery = make_celery(__name__)
# print(my_celery)
# app_celery = create_app(celery=my_celery)

app = create_app(config=config_dict['Debug'],celery=my_celery)

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission,
                Case=Case, Version=Version)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host="0.0.0.0"))


@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.base.models import Role, User
    upgrade()
    Role.insert_roles()
    User.create_superadmin()

@manager.command
def drop():
    Case.drop_cases()

if __name__ == '__main__':
    manager.run()

