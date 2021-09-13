import logging
import os
import jinja2
from flask import Blueprint
import datetime
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

profiles_bp = Blueprint('profiles', __name__)


@profiles_bp.route('/profiles/<string:path>', methods=['GET'])
def profiles(path: str):
    if path == "software-projects":
        template = template_env.get_template(
            'justice-ndou/personal-profile/software-projects/software-projects.html')
        context = {}
    elif path == "linkedin":
        template = template_env.get_template('justice-ndou/personal-profile/linkedin-profile/linkedin.html')
        context = {}

    elif path == "services":
        template = template_env.get_template('justice-ndou/personal-profile/services/services.html')
        context = {}
    else:
        return

    return template.render(context), 200
