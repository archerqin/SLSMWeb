from flask import Blueprint

blueprint = Blueprint(
    'wiki_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='../base/static/assets'
)