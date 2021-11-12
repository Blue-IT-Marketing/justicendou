"""
    Send My Personal Tweets in my own profile

"""
import json
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
        {'created_at': 'Fri Nov 12 08:04:29 +0000 2021',
        'id': 1459069573878235159,
        'id_str': '1459069573878235159',
        'text': 'RT @PhilippeMurer: Raoult balance fort: \n"L\'OMS est achetée par Bill Gates... C\'est le financier majeur de l\'OMS...Vous n\'avez qu\'à regarde…',
        'truncated': False,
        'entities': {'hashtags': [],
                     'symbols': [],
                     'user_mentions': [{'screen_name': 'PhilippeMurer',
                                        'name': 'Philippe Murer 🇫🇷',
                                        'id': 2907408203,
                                        'id_str': '2907408203',
                                        'indices': [3, 17]}],
        'urls': []},
        'metadata': {'iso_language_code': 'fr', 'result_type': 'recent'},
        'source': '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>',
        'in_reply_to_status_id': None,
        'in_reply_to_status_id_str': None,
        'in_reply_to_user_id': None,
        'in_reply_to_user_id_str': None,
        'in_reply_to_screen_name': None,
        'user': {'id': 1380065801395437570,
                 'id_str': '1380065801395437570',
                 'name': 'Nounounath21',
                 'screen_name': 'nounounath21',
                 'location': 'Dijon, France',
                 'description': '',
                 'url': None,
                 'entities': {'description': {'urls': []}},
                 'protected': False,
                 'followers_count': 43,
                 'friends_count': 86,
                 'listed_count': 0,
                 'created_at': 'Thu Apr 08 07:52:58 +0000 2021',
                 'favourites_count': 1598,
                 'utc_offset': None,
                 'time_zone': None,
                 'geo_enabled': False,
                 'verified': False,
                 'statuses_count': 1467,
                 'lang': None,
                 'contributors_enabled': False,
                 'is_translator': False,
                 'is_translation_enabled': False,
                 'profile_background_color': 'F5F8FA',
                 'profile_background_image_url': None,
                 'profile_background_image_url_https': None,
                 'profile_background_tile': False,
                 'profile_image_url': 'http://pbs.twimg.com/profile_images/1443925547822817281/isAsBZxc_normal.jpg',
                 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1443925547822817281/isAsBZxc_normal.jpg',
                 'profile_link_color': '1DA1F2',
                 'profile_sidebar_border_color': 'C0DEED',
                 'profile_sidebar_fill_color': 'DDEEF6',
                 'profile_text_color': '333333',
                 'profile_use_background_image': True,
                 'has_extended_profile': True,
                 'default_profile': True,
                 'default_profile_image': False,
                 'following': False,
                 'follow_request_sent': False,
                 'notifications': False,
                 'translator_type': 'none', 'withheld_in_countries': []},
                 'geo': None,
                 'coordinates': None,
                 'place': None,
                 'contributors': None,
                 'retweeted_status': {'created_at': 'Wed Nov 10 18:56:25 +0000 2021',
                                      'id': 1458508865000116237,
                                      'id_str': '1458508865000116237',
                                      'text': 'Raoult balance fort: \n"L\'OMS est achetée par Bill Gates... C\'est le financier majeur de l\'OMS...Vous n\'avez qu\'à re… https://t.co/5T4zxVQlGZ', 'truncated': True, 'entities': {'hashtags': [], 'symbols': [], 'user_mentions': [], 'urls': [{'url': 'https://t.co/5T4zxVQlGZ', 'expanded_url': 'https://twitter.com/i/web/status/1458508865000116237', 'display_url': 'twitter.com/i/web/status/1…', 'indices': [117, 140]}]}, 'metadata': {'iso_language_code': 'fr', 'result_type': 'recent'}, 'source': '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None, 'user': {'id': 2907408203, 'id_str': '2907408203', 'name': 'Philippe Murer 🇫🇷', 'screen_name': 'PhilippeMurer', 'location': 'France', 'description': "Gaulliste souverainiste/ 3 thèmes essentiels pour la France:économie & social, environnement, flux d'immigration Compte VK https://t.co/iwXkC3Qufg", 'url': None, 'entities': {'description': {'urls': [{'url': 'https://t.co/iwXkC3Qufg', 'expanded_url': 'http://vk.com/PhilippeMurer', 'display_url': 'vk.com/PhilippeMurer', 'indices': [123, 146]}]}}, 'protected': False, 'followers_count': 28112, 'friends_count': 2312, 'listed_count': 154, 'created_at': 'Sat Dec 06 07:25:05 +0000 2014', 'favourites_count': 92232, 'utc_offset': None, 'time_zone': None, 'geo_enabled': False, 'verified': False, 'statuses_count': 43884, 'lang': None, 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': '000000', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1363181524212924416/Or_3dXzG_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1363181524212924416/Or_3dXzG_normal.jpg', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/2907408203/1602157308', 'profile_link_color': '4A913C', 'profile_sidebar_border_color': '000000', 'profile_sidebar_fill_color': '000000', 'profile_text_color': '000000', 'profile_use_background_image': False, 'has_extended_profile': False, 'default_profile': False, 'default_profile_image': False, 'following': False, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none', 'withheld_in_countries': []}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'retweet_count': 2256, 'favorite_count': 4514, 'favorited': False, 'retweeted': False, 'possibly_sensitive': False, 'lang': 'fr'},
                                      'is_quote_status': False,
                                      'retweet_count': 2256,
                                      'favorite_count': 0,
                                      'favorited': False, 'retweeted': False, 'lang': 'fr'}
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
    print(TweeterSearch().search('bill gates')[0]._json)
