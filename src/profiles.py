import os
import jinja2
from flask import Blueprint
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))
profiles_bp = Blueprint('profiles', __name__)


@profiles_bp.route('/profiles/<string:path>', methods=['GET'])
def profiles(path: str):
    """profile routes"""
    software_projects_template = 'justice-ndou/personal-profile/software-projects/software-projects.html'
    linked_in_template = 'justice-ndou/personal-profile/linkedin-profile/linkedin.html'
    services_template = 'justice-ndou/personal-profile/services/services.html'
    return dict(software_projects=template_env.get_template(software_projects_template),
                linkedin=template_env.get_template(linked_in_template),
                services=template_env.get_template(services_template)).get(path.replace('-', '_')).render(dict()), 200
