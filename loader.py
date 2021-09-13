from flask import Flask
from config import Config


def create_app(config=Config):
    app = Flask(__name__, template_folder='resources/templates', static_folder='resources/static')

    with app.app_context():
        from src.blog import blog_handler_bp
        from src.contact import contact_handler_bp, ticket_handler_bp
        from src.navigation import navigation_loader
        from src.profiles import profiles_bp
        from src.services import services_handler_bp
        from src.social import social_handler_bp
        from main import main_router_bp

        app.register_blueprint(blog_handler_bp)
        app.register_blueprint(contact_handler_bp)
        app.register_blueprint(ticket_handler_bp)
        app.register_blueprint(navigation_loader)
        app.register_blueprint(profiles_bp)
        app.register_blueprint(services_handler_bp)

        app.register_blueprint(social_handler_bp)
        app.register_blueprint(main_router_bp)

        return app
