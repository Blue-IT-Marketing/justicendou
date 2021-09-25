from flask import Blueprint, render_template
from src.articles import Articles

cron_route_bp = Blueprint('cron_route', __name__)


@cron_route_bp.route('/_cron/articles', methods=['GET', 'POST'])
def cron_articles():
    Articles().cron_daily_topics()
    return 'OK', 200
