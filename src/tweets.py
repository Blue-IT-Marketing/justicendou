"""
    Send My Personal Tweets in my own profile

"""
import os
from typing import Optional

import tweepy


class TweeterProfile:
    """
        **Tweeter Profile**
            a tweeter bot to manage my tweeter profile

    """

    def __init__(self) -> None:
        self.api_key: str = os.getenv('tweeter_api_key')
        self.access_token: str = os.getenv('tweeter_access_token')
        self.api: Optional[tweepy.API] = None

    def authenticate(self) -> None:
        """
            Authenticate with Twitter API
        """
        auth = tweepy.OAuthHandler(self.api_key, self.access_token)
        self.api = tweepy.API(auth)

    def follow_back(self) -> None:
        """
            Follow back users who follow you
        """
        for follower in tweepy.Cursor(self.api.followers).items():
            if not follower.following:
                follower.follow()

    def un_follow_non_followers(self) -> None:
        """
            Unfollow non-followers
        """
        for user in tweepy.Cursor(self.api.friends).items():
            if not user.following:
                user.unfollow()

    def un_follow_all(self) -> None:
        """
            Unfollow all users
        """
        for user in tweepy.Cursor(self.api.friends).items():
            user.unfollow()

    def send_tweet(self, tweet: str) -> None:
        """
            Send tweet
        """
        self.api.update_status(tweet)

    def send_tweet_with_media(self, tweet: str, media_path: str) -> None:
        """
            Send tweet with media
        """
        self.api.update_with_media(media_path, tweet)


class TweetMessages:
    """
        **Tweet Messages**
    """

    def __init__(self) -> None:
        self.tweet_messages: list = []

    def add_tweet_message(self, tweet_message: str) -> None:
        """
            Add tweet message
        """
        self.tweet_messages.append(tweet_message)

    def get_tweet_message(self) -> str:
        """
            Get tweet message
        """
        return self.tweet_messages[0]

    def remove_tweet_message(self) -> None:
        """
            Remove tweet message
        """
        self.tweet_messages.pop(0)
