from flask import Flask
from config import Config


def create_app(config=Config):
    app = Flask(__name__, template_folder='/resources/templates', static_folder='/resources/static')

    with app.app_context():
        return app
