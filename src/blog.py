import logging
import os
import jinja2
from flask import Blueprint, render_template, request
import datetime

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

blog_handler_bp = Blueprint('blog_handler', __name__)


def get_url(path: str) -> str:
    return path.split('?')[0]

# TODO- consider methods of obtaining and storing old articles and then submitting them as secong pages indexed by dates


@blog_handler_bp.route('/blog/<string:path>', methods=['POST', 'GET'])
def blog_handler(path: str):
    request_url_list = get_url(path).split("/")
    this_url = request_url_list[len(request_url_list) - 1]
    if request.method == 'GET':
        if this_url == "programming":
            template = template_env.get_template('templates/justice-ndou/blog/categories/programming/programming.html')
            return render_template(template)

        elif this_url == "science":
            template = template_env.get_template('templates/justice-ndou/blog/categories/science/science.html')
            return render_template(template)

        elif this_url == "philosophy":
            template = template_env.get_template('templates/justice-ndou/blog/categories/philosophy/philosophy.html')
            return render_template(template)

        elif this_url == "mathematics":
            template = template_env.get_template('templates/justice-ndou/blog/categories/mathematics/mathematics.html')
            return render_template(template)

        elif this_url == "hacking":
            template = template_env.get_template('templates/justice-ndou/blog/categories/hacking/hacking.html')
            return render_template(template)

        elif this_url == "networking":
            template = template_env.get_template('templates/justice-ndou/blog/categories/networking/networking.html')
            return render_template(template)

        elif this_url == "ai":
            template = template_env.get_template('templates/justice-ndou/blog/categories/ai/ai.html')
            return render_template(template)


@blog_handler_bp.route('/topics/<string:path>', methods=['POST', 'GET'])
def topics_handler(path: str):
    pass
