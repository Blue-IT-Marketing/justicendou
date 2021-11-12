
from google.cloud import ndb


class TweetModel(ndb.Model):
    """
        **A Google Datastore Model to store Tweets**
    """
    tweet_id: str = ndb.StringProperty()
    tweet_text: str = ndb.StringProperty()
    tweet_created_at: str = ndb.StringProperty()
    tweet_user_id: str = ndb.StringProperty()
    tweet_user_name: str = ndb.StringProperty()
    tweet_user_screen_name: str = ndb.StringProperty()
    tweet_user_location: str = ndb.StringProperty()
    tweet_user_description: str = ndb.StringProperty()
    tweet_user_followers_count: int = ndb.IntegerProperty()
    tweet_user_friends_count: int = ndb.IntegerProperty()
    tweet_user_listed_count: int = ndb.IntegerProperty()


    








    