import os
import jinja2
from flask import Blueprint, request, render_template
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

navigation_loader = Blueprint('navigation_loader', __name__)


@navigation_loader.route('/navigation/<string:path>', methods=['GET', 'POST'])
def navigation(path: str):
    """**navigation**
    routes"""
    return dict(header=template_env.get_template('dynamic/navigation/header.html'),
                sidebar=template_env.get_template('dynamic/navigation/sidebar.html'),
                footer=template_env.get_template('dynamic/navigation/footer.html')).get(path).render(dict()), 200
