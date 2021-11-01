import os
import jinja2
from flask import Blueprint

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))
social_handler_bp = Blueprint('social_handler', __name__)


@social_handler_bp.route('/social/<string:path>', methods=['POST', 'GET'])
def social_handler(path: str):
    """select and returns a social profile base on path"""
    
    return dict(facebook=template_env.get_template('justice-ndou/social/facebook.html'),
    google=template_env.get_template('justice-ndou/social/google.html'),
    twitter=template_env.get_template('justice-ndou/social/twitter.html'),
    youtube=template_env.get_template('justice-ndou/social/youtube.html'),
    quora=template_env.get_template('justice-ndou/social/quora.html')).get(path).render(dict()), 200
