import asyncio
from datetime import datetime, date
import os
from typing import Optional, List, Coroutine
import requests
from decouple import config
from flask import Blueprint
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadValueError

from src.contact import create_id
from src.fetch_utils import async_get_request

this_topics = ["CyberAttacks", "Hacking Tools", "Linux", "Kali Linux", "Hacking", "Hackers", "Penetration Testing",
               "Algorithms", "Botnets",
               "Crypto Mining", "New Crypto Coins", "Crypto Coins", "DDOS", "Networking", "State Sponsored Hacking",
               "State Sponsored Malware",
               "Mathematics", "Mathematics in Programing", "Numerical Algorithms", "Graph Theory", "Cryptography",
               "Numerical Analysis", "Signal Processing", "Fourier Transforms", "Laplace Transforms", "Combinatorial",
               "Theory of Everything", "Quantum Mechanics", "Python", "Programming", "Algorithms", "Google App Engine",
               "Javascript", "Angular", "React", "Typescript", "HTML5",
               "CSS3", "Jquery", "Server Side Rendering", "NODEJS", "NODE", "NPM", "Jinja2", "Jinja Templating",
               "Physics", "Nano Technology", "Space Exploration", "SpaceX", "Advanced Physics", "Moon", "Mars",
               "Astronomy",
               "Astrophysics", "Chemical Engineering"]

this_page_size = 50

apiKey = config('articles_api_key') or os.getenv('articles_api_key')


class Interests(ndb.Model):
    topic_id = ndb.StringProperty()
    topic = ndb.StringProperty()
    topic_active = ndb.BooleanProperty(default=True)

    @staticmethod
    def add_default_topics(self):
        for topic in this_topics:
            interest_instance = Interests.query(Interests.topic == topic).get()
            if not isinstance(interest_instance, Interests) or not interest_instance.topic:
                interest_instance = Interests(topic_id=create_id(), topic=topic, topic_active=True)
                interest_instance.put()

    @staticmethod
    def add_topic(topic) -> ndb.Key:
        if topic:
            interest_instance = Interests.query(Interests.topic == topic).get()
            if not isinstance(interest_instance, Interests) or not interest_instance.topic:
                interest_instance = Interests(topic_id=create_id(), topic=topic, topic_active=True)
                return interest_instance.put()

    @staticmethod
    def get_all_topics() -> List[dict]:
        return [topic.to_dict() for topic in Interests.query().fetch()]


class Articles(ndb.Model):
    article_reference = ndb.StringProperty()
    topic = ndb.StringProperty()
    url = ndb.StringProperty()
    title = ndb.StringProperty()
    article_link = ndb.StringProperty()
    urlToImage = ndb.StringProperty()
    description = ndb.StringProperty()
    date_created = ndb.DateProperty(auto_now_add=True)

    @staticmethod
    def fetch_random_articles() -> Optional[dict]:
        """
            **fetch_random_articles**

        """
        import random
        return asyncio.run(Articles.fetch_articles_by_topic(topic=random.choice(this_topics)))

    @staticmethod
    async def fetch_articles_by_topic(topic: str) -> Optional[dict]:
        """
            **fetch_articles_by_topic**
        """
        try:
            headers = {'Content-Type': 'application/json'}
            my_articles_url = Articles.return_articles_url(topic)
            result, status_code = await async_get_request(_url=my_articles_url, headers=headers)
            return result if status_code == 200 else None

        except requests.ConnectionError:
            return None
        except requests.Timeout:
            return None

    @staticmethod
    def return_articles_url(topic):
        """
            **return_articles_url**
        :param topic:
        :return:
        """
        articles_url = 'https://newsapi.org/v2/everything?q='
        my_date = datetime.now().date()
        formatted_date: str = f'{my_date.year}-{my_date.month}-{my_date.day}'
        my_articles_url = articles_url + topic + "&language=en" + "&from=" + formatted_date + "&apiKey=" + apiKey
        return my_articles_url

    def get_articles(self) -> List[tuple]:
        _articles_cron: List[Coroutine] = [self.fetch_articles_by_topic(topic=topic) for topic in this_topics]
        responses = asyncio.run(asyncio.gather(*_articles_cron))
        return [(this_topics[idx], _response.result()) for idx, _response in enumerate(responses)]

    @ndb.toplevel
    def cron_daily_topics(self) -> None:
        response = [self.compile_save_article(articles, topic) for topic, articles in self.get_articles()]

    @staticmethod
    @ndb.tasklet
    def compile_save_article(articles, topic) -> ndb.Key:
        """
        **compile_save_article**
            given the articles save them under the specified topic and await key
        :param articles:
        :param topic:
        :return:
        """
        _article = articles['articles']
        article_instance: Articles = Articles()
        article_instance.topic = topic
        article_instance.url = _article.get('url')
        article_instance.title = _article.get('title')
        link_slug: str = Articles.create_unique_slug_from_topic_title(topic=topic, title=_article.get('title'))
        article_instance.article_link = link_slug
        article_instance.urlToImage = _article.get('urlToImage')

        article_instance.description = _article.get('description')
        article_instance.article_reference = create_id()
        return article_instance.put_async().get_result()

    @staticmethod
    def create_unique_slug_from_topic_title(topic, title) -> str:
        topic_slug = "".join(topic.split(" "))
        title_slug = "".join(title.split(" "))
        return f"{topic_slug}/{datetime.now().date()}/{title_slug}"

    # Search methods
    @staticmethod
    def get_articles_by_topic(topic):
        article_query = Articles.query(Articles.topic == topic).order(Articles.date_created).fetch(limit=1000)
        return [article.to_dict() for article in article_query]

    @staticmethod
    def get_articles_by_date_topic_(topic, article_date: date) -> List[dict]:
        article_query = Articles.query(Articles.topic == topic).order(Articles.date_created).fetch(limit=1000)
        return [article.to_dict() for article in article_query]

    @staticmethod
    def get_all_articles_by_date(by_date: date) -> List[dict]:
        article_query = Articles.query(Articles.date_created == by_date).order(Articles.date_created).fetch(limit=1000)
        return [article.to_dict() for article in article_query]


articles_route_bp = Blueprint('articles_route', __name__)


@articles_route_bp.route('/article/<string:path>', methods=['GET'])
def article(article: str) -> tuple:
    """

    :param article:
    :return:
    """
    pass
