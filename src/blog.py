import os

import jinja2
from flask import Blueprint, render_template

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

blog_handler_bp = Blueprint('blog_handler', __name__)


def get_url(path: str) -> str:
    return path.split('?')[0]


# TODO- consider methods of obtaining and storing old articles and then submitting them as secong pages indexed by dates


@blog_handler_bp.route('/blog/<string:path>', methods=['GET'])
def blog_handler(path: str):
    # Will throw an error if route/ template not found
    template_lookup: dict = dict(
        programming=template_env.get_template('justice-ndou/blog/categories/programming/programming.html'),
        science=template_env.get_template('justice-ndou/blog/categories/science/science.html'),
        philosophy=template_env.get_template('justice-ndou/blog/categories/philosophy/philosophy.html'),
        mathematics=template_env.get_template('justice-ndou/blog/categories/mathematics/mathematics.html'),
        hacking=template_env.get_template('justice-ndou/blog/categories/hacking/hacking.html'),
        networking=template_env.get_template('justice-ndou/blog/categories/networking/networking.html'),
        ai=template_env.get_template('justice-ndou/blog/categories/ai/ai.html')
    )

    request_url_list = get_url(path).split("/")
    return render_template(template_lookup[request_url_list[-1]])


@blog_handler_bp.route('/topics/<string:path>', methods=['POST', 'GET'])
def topics_handler(path: str):
    pass
