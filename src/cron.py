from flask import Blueprint, render_template
from flask import current_app
from threading import Thread
from src.articles import Articles

cron_route_bp = Blueprint('cron_route', __name__)


@cron_route_bp.route('/_cron/articles', methods=['GET', 'POST'])
def cron_articles():
    """
        **cron_articles**
            run cron articles in a separate thread
    :return:
    """
    current_app.articles_cron_jobs = Thread(target=Articles().cron_daily_topics)
    try:
        current_app.articles_cron_jobs.run()
    except RuntimeError:
        return 'Error', 500
    return 'OK', 200
