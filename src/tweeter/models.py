
from google.cloud import ndb


class TweetModel(ndb.Model):
    """
        **A Google Datastore Model to store Tweets**
    """
    tweet_id: str = ndb.StringProperty()
    id_str: str = ndb.StringProperty()
    text: str = ndb.StringProperty()
    created_at: str = ndb.StringProperty()
    user_id: str = ndb.StringProperty()
    user_name: str = ndb.StringProperty()
    user_screen_name: str = ndb.StringProperty()
    user_location: str = ndb.StringProperty()
    user_description: str = ndb.StringProperty()
    user_followers_count: int = ndb.IntegerProperty()
    user_friends_count: int = ndb.IntegerProperty()
    user_listed_count: int = ndb.IntegerProperty()


    








    