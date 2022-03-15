import os
from app import create_app, db
from app.base.models import *
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from config import config_dict
# import MySQLdb

app = create_app(config_dict['Debug'])
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

