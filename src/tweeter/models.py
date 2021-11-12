
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


    def __str__(self) -> str:
        """string represantation of tweet"""
        return f"id: {self.tweet_id} tweeted by: {self.user_screen_name} tweet: {self.text}"


    def consume_tweet(self, tweet) -> ndb.Key:
        """
            **Consumes a tweet and stores it in the datastore**
        """
        self.tweet_id = tweet.id
        self.id_str = tweet.id_str
        self.text = tweet.text
        self.created_at = tweet.created_at
        self.user_id = tweet.user.id
        self.user_name = tweet.user.name
        self.user_screen_name = tweet.user.screen_name
        self.user_location = tweet.user.location
        self.user_description = tweet.user.description
        self.user_followers_count = tweet.user.followers_count
        self.user_friends_count = tweet.user.friends_count
        self.user_listed_count = tweet.user.listed_count
        return self.put()








    