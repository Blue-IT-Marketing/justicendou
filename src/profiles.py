import os
import jinja2
from flask import Blueprint
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

profiles_bp = Blueprint('profiles', __name__)


@profiles_bp.route('/profiles/<string:path>', methods=['GET'])
def profiles(path: str):
    """profile routes"""
    if path == "software-projects":
        template = template_env.get_template(
            'justice-ndou/personal-profile/software-projects/software-projects.html')
        context = dict()
    elif path == "linkedin":
        template = template_env.get_template('justice-ndou/personal-profile/linkedin-profile/linkedin.html')
        context = dict()

    elif path == "services":
        template = template_env.get_template('justice-ndou/personal-profile/services/services.html')
        context = dict()
    else:
        return

    return template.render(context), 200
