import os
import jinja2
import logging
import datetime
import json
import requests
from google.cloud import ndb


this_topics = ["CyberAttacks","Hacking Tools","Linux","Kali Linux","Hacking","Hackers","Penetration Testing","Algorithms","Botnets",
               "Crypto Mining","New Crypto Coins","Crypto Coins","DDOS","Networking","State Sponsored Hacking","State Sponsored Malware",
               "Mathematics","Mathematics in Programing","Numerical Algorithms","Graph Theory","Cryptography",
               "Numerical Analysis","Signal Processing","Fourier Transforms","Laplace Transforms","Combinatorials",
               "Theory of Everything", "Quantum Mechanics", "Python", "Programming", "Algorithms", "Google App Engine","Javascript", "Angular", "React", "Typescript","HTML5",
               "CSS3","Jquery","Server Side Rendering","NODEJS","NODE","NPM","Jinja2","Jinja Templating",
               "Physics","Nanotechnolodgy","Space Exploration","SpaceX","Advanced Physics","Moon","Mars","Astronomy",
               "Astrophysics","Chemical Engineering"]

this_page_size = 50

apiKey = '41e896a0a1c94b61903408fae1a49471'


def convert_datestring_to_datetime(date_string):
    try:
        date_string = str(date_string)
        try:
            date_list = date_string.split("\\")
            my_year = int(date_list[0])
            my_month = int(date_list[1])
            my_day = int(date_list[2])
        except:
            date_list = date_string.split("-")

            if len(date_list) == 3:
                my_year = int(date_list[0])
                my_month = int(date_list[1])
                my_day = int(date_list[2])
            else:
                this_date = datetime.datetime.now()
                this_date = this_date.date()
                my_year = this_date.year
                my_month = this_date.month
                my_day = this_date.day

        this_date = datetime.date(year=my_year, month=my_month, day=my_day)

        return this_date


    except Exception as e:
        raise e


class Interests(ndb.Expando):
    _sep = ":"
    topic_id = ndb.StringProperty()
    topic = ndb.StringProperty()
    subjects = ndb.StringProperty()

    topic_active = ndb.BooleanProperty(default=True)

    def write_topic_id(self, id):
        try:
            id = str(id)
            if id is not None:
                self.topic_id = id
                return True
            else:
                return False

        except Exception as e:
            raise e

    def write_topic(self, topic):
        try:
            topic = str(topic)
            if topic is not None:
                self.topic = topic
                return True
            else:
                return False
        except Exception as e:
            raise e

    def write_subjects(self, subject):
        try:
            subject = str(subject)
            logging.info(subject)
            if subject is not None:
                if (self.subjects is not None) and len(self.subjects) != 0:
                    self.subjects += self._sep + subject
                else:
                    self.subjects = subject
                return True
            else:
                return False
        except Exception as e:
            logging.warning(subject)

            raise e

    def set_topic_active(self, value):
        try:
            if value in [True, False]:
                self.topic_active = value
                return True
            else:
                return False
        except Exception as e:
            raise e


class Articles(ndb.Expando):
    article_reference = ndb.StringProperty()
    topic = ndb.StringProperty()
    url = ndb.StringProperty()
    title = ndb.StringProperty()
    urlToImage = ndb.StringProperty()
    description = ndb.StringProperty()
    this_date = ndb.DateProperty(auto_now_add=True)

    def write_topic(self, topic):
        try:
            if topic is not None:
                self.topic = topic
                return True
            else:
                return False

        except:
            return False

    @staticmethod
    def create_reference():
        import random, string
        try:
            reference = ""
            for i in range(256):
                reference += random.SystemRandom().choice(string.digits + string.ascii_lowercase)
            return reference
        except:
            return ""

    def write_reference(self, ref):
        try:
            if ref != "":
                self.article_reference = ref
                return True
            else:
                return False
        except:
            return False

    def write_url(self, url):
        try:
            url = str(url)
            if url is not None:
                self.url = url
                return url
        except Exception as e:
            raise e

    def write_title(self, title):
        try:
            title = str(title)
            title = title.strip()
            if title is not None:
                self.title = title
                return True
            else:
                return False

        except Exception as e:
            raise e

    def write_url_to_image(self, url_to_image):
        try:
            url_to_image = str(url_to_image)
            if url_to_image is not None:
                self.urlToImage = url_to_image
                return True
            else:
                return False
        except Exception as e:
            raise e

    def write_description(self, description):
        try:
            description = str(description)
            description = description.strip()
            if description is not None:
                self.description = description
                return True
            else:
                return False
        except Exception as e:
            raise e

    @staticmethod
    def fetch_articles(total):
        """

        """
        try:
            import random
            articles_url = 'https://newsapi.org/v2/everything?q='
            my_date = datetime.datetime.now()
            this_date = str(my_date.year) + "-" + str(my_date.month) + "-" + str(my_date.day)

            my_articles_url = articles_url + random.choice(
                this_topics) + '&language=en' + '&from=' + this_date + '&apiKey=' + apiKey

            headers = {'Content-Type': 'text/html'}
            result = requests.get(url=my_articles_url, headers=headers, validate_certificate=True)

            try:
                if result.status_code == 200:
                    my_json = json.loads(result.content)
                    return my_json
                else:
                    return "{STATUS : " + str(result.status_code) + "}"
            except Exception as e:
                logging.info(e)
                raise e

        except Exception as e:
            logging.info(e)
            return {"Message": "There was an error accessing NEWS API"}

    @staticmethod
    def fetch_topic(topic):
        """
        """
        try:
            articles_url = 'https://newsapi.org/v2/everything?q='
            my_date = datetime.datetime.now()
            this_date = str(my_date.year) + "-" + str(my_date.month) + "-" + str(my_date.day)

            my_articles_url = articles_url + topic + "&language=en" + "&from=" + this_date + "&apiKey=" + apiKey

            headers = {'Content-Type': 'text/html'}
            result = requests.get(url=my_articles_url, headers=headers, validate_certificate=True)

            try:
                if result.status_code == 200:
                    return json.loads(result.content)
                else:
                    return ""
            except Exception:
                pass

        except Exception:
            return ""

    def save_topics(self):
        try:

            for topic in this_topics:
                json_results = self.fetch_topic(topic=topic)
                if json_results != "":
                    articles = json_results['articles']

                    this_date = datetime.datetime.now()
                    this_date = this_date.date()

                    for article in articles:
                        self.write_url(url=article['url'])
                        self.write_title(title=article['title'])
                        self.write_url_to_image(url_to_image=article['urlToImage'])
                        self.write_description(description=article['description'])
                        self.write_reference(ref=self.create_reference())
                        self.put()
                else:
                    pass
        except Exception as e:
            raise e


class Posts(ndb.Expando):
    """
        this is for the blog
    """

    post_url = ndb.StringProperty()
    post_title = ndb.StringProperty()
    post_description = ndb.StringProperty()
    post_body = ndb.StringProperty()

    post_date = ndb.DateProperty()
    post_time = ndb.TimeProperty()

    post_category = ndb.StringProperty()

    post_seo_description = ndb.StringProperty()

    def write_post_url(self, post_url):
        try:
            post_url = str(post_url)
            post_url = post_url.strip()

            if post_url is not None:
                self.post_url = post_url
                return True
            else:
                return False
        except Exception as e:
            raise e

    def write_post_title(self, post_title):
        try:
            post_title = str(post_title)
            post_title = post_title.strip()
            if post_title is not None:
                self.post_title = post_title
                return True
            else:
                return False
        except Exception as e:
            raise e

    def write_post_description(self, post_description):
        try:
            post_description = str(post_description)
            post_description = post_description.strip()
            if post_description is not None:
                self.post_description = post_description
                return True
            else:
                return False

        except Exception as e:
            raise e

    def write_post_body(self, post_body):
        try:
            post_body = str(post_body)
            post_body = post_body.strip()

            if post_body is not None:
                self.post_body = post_body
                return True
            else:
                return False
        except Exception as e:
            raise e

    def write_post_date(self, post_date):
        try:

            if isinstance(post_date, datetime.date):
                self.post_date = post_date
                return True
            else:
                return False

        except Exception as e:
            raise e

    def write_post_time(self, post_time):
        try:

            if isinstance(post_time, datetime):
                self.post_time = post_time
                return True
            else:
                return False

        except Exception as e:
            raise e

    def write_post_category(self, post_category):
        try:

            post_category = str(post_category)
            if post_category is not None:
                self.post_category = post_category
                return True
            else:
                return False

        except Exception as e:
            raise e

    def write_post_seo_description(self, post_seo_description):
        try:

            post_seo_description = str(post_seo_description)
            post_seo_description = post_seo_description.strip()

            if post_seo_description is not None:
                self.post_seo_description = post_seo_description
                return True
            else:
                return False

        except Exception as e:
            raise e