"""
    Send My Personal Tweets in my own profile

"""
import tweepy


class TweeterProfile:
    """
        **Tweeter Profile**

    """
    def __init__(self) -> None:
        self.api_key: str = os.getenv('tweeter_api_key')
        self.access_token: str = os.getenv('tweeter_access_token')

    def authenticate(self) -> None:
        """
            Authenticate with Twitter API
        """
        auth = tweepy.OAuthHandler(self.api_key, self.access_token)
        api = tweepy.API(auth)
        return api

    def follow_back(self, api: tweepy.API) -> None:
        """
            Follow back users who follow you
        """
        for follower in tweepy.Cursor(api.followers).items():
            if not follower.following:
                follower.follow()

    
    def un_follow_non_followers(self, api: tweepy.API) -> None:
        """
            Unfollow non-followers
        """
        for user in tweepy.Cursor(api.friends).items():
            if not user.following:
                user.unfollow()

    def un_follow_all(self, api: tweepy.API) -> None:
        """
            Unfollow all users
        """
        for user in tweepy.Cursor(api.friends).items():
            user.unfollow()

    def send_tweet(self, api: tweepy.API, tweet: str) -> None:
        """
            Send tweet
        """
        api.update_status(tweet)

    def send_tweet_with_media(self, api: tweepy.API, tweet: str, media_path: str) -> None:
        """
            Send tweet with media
        """
        api.update_with_media(media_path, tweet)

