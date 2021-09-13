import os

import jinja2
from flask import Blueprint

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

social_handler_bp = Blueprint('social_handler', __name__)


@social_handler_bp.route('/social/<string:path>', methods=['POST', 'GET'])
def social_handler(path: str):
    if path == "facebook":
        template = template_env.get_template('justice-ndou/social/facebook.html')
        context = {}
        return template.render(context), 200

    elif path == "google":
        template = template_env.get_template('justice-ndou/social/google.html')
        context = {}
        return template.render(context), 200

    elif path == "twitter":
        template = template_env.get_template('justice-ndou/social/twitter.html')
        context = {}
        return template.render(context), 200

    elif path == "youtube":
        template = template_env.get_template('justice-ndou/social/youtube.html')
        context = {}
        return template.render(context), 200

    elif path == "quora":
        template = template_env.get_template('justice-ndou/social/quora.html')
        context = {}
        return template.render(context), 200
