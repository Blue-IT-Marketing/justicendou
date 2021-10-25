import os
import jinja2
from flask import Blueprint, request, render_template
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))
# 0763088022
navigation_loader = Blueprint('navigation_loader', __name__)


@navigation_loader.route('/navigation/<string:path>', methods=['GET', 'POST'])
def navigation(path: str):
    """navigation routes"""
    if path == "header":
        template = template_env.get_template('dynamic/navigation/header.html')
        context = dict()
        return template.render(context), 200
    elif path == "sidebar":
        template = template_env.get_template('dynamic/navigation/sidebar.html')
        context = dict()
        return template.render(context), 200
    elif path == "footer":
        template = template_env.get_template('dynamic/navigation/footer.html')
        context = dict()
        return template.render(context), 200
    else:
        pass
