import asyncio
import os
from datetime import datetime, date
from typing import Optional, List, Coroutine

import requests
from decouple import config
from flask import Blueprint, render_template
from google.cloud import ndb

from src.contact import create_id
from src.fetch_utils import async_get_request
from src.use_context import use_context

default_topics = ["CyberAttacks", "Hacking Tools", "Linux", "Kali Linux", "Hacking", "Hackers", "Penetration Testing",
                  "Algorithms", "Botnets",
                  "Crypto Mining", "New Crypto Coins", "Crypto Coins", "DDOS", "Networking", "State Sponsored Hacking",
                  "State Sponsored Malware",
                  "Mathematics", "Mathematics in Programing", "Numerical Algorithms", "Graph Theory", "Cryptography",
                  "Numerical Analysis", "Signal Processing", "Fourier Transforms", "Laplace Transforms",
                  "Combinatorial",
                  "Theory of Everything", "Quantum Mechanics", "Python", "Programming", "Algorithms",
                  "Google App Engine",
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
    def add_default_topics():
        for topic in default_topics:
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
        return asyncio.run(Articles.fetch_articles_by_topic(topic=random.choice(default_topics)))

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
        base_url = 'https://newsapi.org/v2/everything?q='
        my_date = datetime.now().date()
        formatted_date: str = f'{my_date.year}-{my_date.month}-{my_date.day}'
        return f'{base_url}{topic}&language=en&from={formatted_date}&apiKey={apiKey}'

    def get_articles(self) -> List[tuple]:
        _articles_cron: List[Coroutine] = [self.fetch_articles_by_topic(topic=topic) for topic in default_topics]
        responses = asyncio.run(asyncio.gather(*_articles_cron))
        return [(default_topics[idx], _response.result()) for idx, _response in enumerate(responses)]

    @ndb.toplevel
    def cron_daily_topics(self) -> None:
        [self.compile_save_article(_articles, topic) for topic, _articles in self.get_articles()]

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
    @use_context
    def get_articles_by_topic(topic):
        article_query = Articles.query(Articles.topic == topic).order(Articles.date_created).fetch(limit=1000)
        return [_article.to_dict() for _article in article_query]

    @staticmethod
    @use_context
    def get_articles_by_date_topic_(topic, article_date: date) -> List[dict]:
        article_query = Articles.query(Articles.topic == topic).order(Articles.date_created).fetch(limit=1000)
        return [_article.to_dict() for _article in article_query]

    @staticmethod
    @use_context
    def get_all_articles_by_date(by_date: date) -> List[dict]:
        article_query = Articles.query(Articles.date_created == by_date).order(Articles.date_created).fetch(limit=1000)
        return [_article.to_dict() for _article in article_query]

    @staticmethod
    @use_context
    def get_article_by_link(link_slug: str):
        article_instance: Articles = Articles.query(Articles.article_link == link_slug).get()
        if isinstance(article_instance, Articles) and article_instance.article_link:
            return article_instance.to_dict()
        return None


articles_route_bp = Blueprint('articles_route', __name__)


@articles_route_bp.route('/article/<string:topic>/<string:article_date>/<string:title_slug>', methods=['GET'])
def article(topic: str, article_date: str, title_slug: str) -> tuple:
    """
        **article**

    :param topic:
    :param article_date:
    :param title_slug
    :return:
    """

    link_slug: str = f'{topic}/{article_date}/{title_slug}'
    article_data: Optional[dict] = Articles.get_article_by_link(link_slug=link_slug)
    return render_template('blog/articles.html', article=article_data), 200


hacking_topics: List[str] = ["CyberAttacks", "Hacking Tools", "Linux", "Kali Linux", "Hacking",
                             "Penetration Testing Algorithms", "Botnets", "Botnet Mining", "Hackers",
                             "Penetration Testing", "DDOS", "Networking", "State Sponsored Hacking"]


def route_articles():
    """
        **route_articles**
    :return:
    """
    default_subjects: List[str] = ['Hacking', 'Mathematics', 'Networking', 'Programming', 'Science', 'Philosophy']
    article_list: List[dict] = Articles.get_articles_by_topic(topic=hacking_topics[0])
    for topic in hacking_topics[1:]:
        article_list += Articles.get_articles_by_topic(topic=topic)
    return render_template("blog/blog.html", subjects=sorted(default_subjects), article_list=article_list,
                           selected_subject='hacking'), 200


@articles_route_bp.route('/articles', methods=['GET'])
def articles():
    return route_articles()
