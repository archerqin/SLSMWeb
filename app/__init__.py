from flask import Flask
from celery import Celery
# from flask_bootstrap import Bootstrap
from flask_moment import Moment
# from flask_sqlalchemy import SQLAlchemy
from exts import db
from flask_login import LoginManager,current_user
from flask_pagedown import PageDown
import celery_config as celery_config
# from config import config
from importlib import import_module
from functools import wraps


# bootstrap = Bootstrap()
# db = SQLAlchemy()
moment = Moment()
pagedown = PageDown()

celery_config=celery_config

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)

def register_blueprint(app):
    for module_name in ('base','home','wiki', 'dev'):
        module = import_module('app.{}.views'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

##在工厂函数中创建Celery实例，加载配置，并实现Flask程序上下文支持
def register_celery(celery, app):
    celery.config_from_object(celery_config)
    class ContextTask(celery.Task):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

def create_app(**kwargs):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(kwargs.get('config'))
    
    register_extensions(app)
    register_blueprint(app)
    configure_database(app)

    ##注册celery
    register_celery(kwargs.get('celery'), app=app)

    return app

class Permission:
    COMMIT = 0x01
    FINISH = 0x02
    VERSION = 0x04
    ADMIN = 0x7f
    SuperAdmin = 0xff

##decorator
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f) or permission_required(Permission.SuperAdmin)(f)

def superadmin_required(f):
    return permission_required(Permission.SuperAdmin)(f)