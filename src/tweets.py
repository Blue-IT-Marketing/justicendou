"""
    Send My Personal Tweets in my own profile

"""
import time
from typing import List

import decouple
import tweepy


class TweetFeed:
    """
        Tweeter Messages
    """
    def __init__(self):
        self.tweeter_handle: str = ''
        self.tweet_id: str = ''
        self.tweet: str = ''


class TweeterAuth:
    """
        Authenticate with tweeter
    """
    def __init__(self) -> None:
        self.api_key: str = decouple.config('tweeter_api_key')
        self.api_key_secret: str = decouple.config('tweeter_api_secret')
        self.access_token: str = decouple.config('tweeter_access_token')
        self.access_token_secret: str = decouple.config('tweeter_access_token_secret')
        self.bearer_token: str = decouple.config('tweeter_bearer_token')

    def oauth2(self):
        auth = tweepy.OAuthHandler(consumer_key=self.api_key, consumer_secret=self.api_key_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return auth


class TweeterSearch(TweeterAuth):
    """
        Searches Tweeter and returns a list of results
    """
    def __init__(self):
        super().__init__()
        self.api: tweepy.API = tweepy.API(self.oauth2())
        self.result_limit: int = 100

    def search(self, search_term: str) -> list:
        return [_tweet for _tweet in tweepy.Cursor(self.api.search_tweets, q=search_term).items(self.result_limit)]


class TweeterProfile(TweeterAuth):
    """
        **Tweeter Profile**
            a tweeter bot to manage my tweeter profile

    """

    def __init__(self) -> None:
        # initialize and authenticate with tweeter
        super().__init__()
        self.api: tweepy.API = tweepy.API(self.oauth2())

    def update_status(self, _tweet: str) -> None:
        """creates a status update on tweeter"""
        self.api.update_status(status=_tweet)

    def send_tweet_with_media(self, tweet: str, media_path: str) -> None:
        """
            Send tweet with media
        """
        self.api.update_status_with_media(status=tweet, media_path=media_path)


class TweeterFollowBot(TweeterAuth):
    """
        **TweeterFollowBot**
            Twitter follow bot uses a strategy to maximise user follows
    """
    def __init__(self):
        """"""
        super().__init__()
        self.api: tweepy.API = tweepy.API(self.oauth2())

    def follow_back(self) -> list:
        """
            Follow a user who follows you
        """
        return [follower.unfollow() for follower in self.api.get_followers() if follower.following]

    def un_follow_non_followers(self) -> list:
        """
            Unfollow non-followers
            followers
            :return unfollowed users
        """
        return [_follower.unfollow() for _follower in self.api.get_followers() if not _follower.following]

    def un_follow_all(self) -> list:
        """

            Unfollow all users
            friends are users i follow
        """
        return [_user.unfollow() for _user in self.api.get_friends()]


if __name__ == '__main__':
    i = 0
    while i < 50:
        TweeterFollowBot().un_follow_all()
        time.sleep(i*10)
        i += 1
