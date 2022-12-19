from flask import Blueprint

blueprint = Blueprint(
    'dev_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)