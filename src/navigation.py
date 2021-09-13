import os
import jinja2
from flask import Blueprint, request
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

navigation_loader = Blueprint('navigation_loader', __name__)


@navigation_loader.route('/navigation/<string:path>', methods=['GET', 'POST'])
def navigation(path: str):
    if path == "header":
        template = template_env.get_template('templates/dynamic/navigation/header.html')
        context = {}
        return template.render(context), 200
    elif path == "sidebar":
        template = template_env.get_template('templates/dynamic/navigation/sidebar.html')
        context = {}
        return template.render(context), 200
    elif path == "footer":
        template = template_env.get_template('templates/dynamic/navigation/footer.html')
        context = {}
        return template.render(context), 200
    else:
        pass

