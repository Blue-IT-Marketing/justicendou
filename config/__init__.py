"""
    **Flask App Configuration Settings**
    *Python Version 3.8 and above*
    Used to setup environment variables for python flask app
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import os
import typing
# noinspection PyPackageRequirements
from decouple import config
import datetime


class Config:
    """
        **APP Configuration Settings**
            configuration variables for setting up the application
    """
    # TODO - Clean up configuration settings
    def __init__(self) -> None:
        # APP URLS
        self.BASE_URL: str = os.environ.get("BASE_URL") or config("BASE_URL")
        self.APP_ID: str = ""
        self.SEP: str = "#"

        self.SMTP_SERVER_URI: str = os.environ.get("SMTP_SERVER_URI") or config("SMTP_SERVER_URI")
        self.SMTP_SERVER_PASSWORD: str = os.environ.get("SMTP_SERVER_PASSWORD") or config("SMTP_SERVER_PASSWORD")
        self.SMTP_SERVER_USERNAME: str = os.environ.get("SMTP_SERVER_USERNAME") or config("SMTP_SERVER_USERNAME")

        self.PROJECT: str = os.environ.get("PROJECT") or config("PROJECT")
        self.APP_NAME: str = os.environ.get("APP_NAME") or config("APP_NAME")

        self.IS_PRODUCTION: bool = True
        self.SECRET_KEY: str = os.environ.get("SECRET_KEY") or config("SECRET_KEY")
        self.DEBUG: bool = False

        self.CACHE_TYPE: str = "simple"
        self.CACHE_DEFAULT_TIMEOUT: int = 60 * 60 * 6
        self.GOOGLE_APPLICATION_CREDENTIALS: str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        self.ENV: str = "production"
        self.TEMPLATES_AUTO_RELOAD: bool = True
        self.PREFERRED_URL_SCHEME: str = "https"

        self.CRON_DOMAIN: str = os.environ.get("CRON_DOMAIN") or config("CRON_DOMAIN")
        self.CRON_SECRET: str = config("CRON_SECRET") or config("CRON_SECRET")

        # NOTE : setting IS_PRODUCTION here - could find a better way of doing this rather
        # than depending on the OS
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()

    def cache_dict(self) -> dict:
        """
            Consider converting the cache to MEM_CACHE Type or Redis
            preferably host the cache as a docker instance on Cloud Run
        :return: dict
        """
        # TODO : use memcached on docker
        return {
            "CACHE_TYPE": "simple",
            "CACHE_DEFAULT_TIMEOUT": self.CACHE_DEFAULT_TIMEOUT,
            "CACHE_KEY_PREFIX": "memberships_cache_"
        }


config_instance: Config = Config()
# Note: Config is a singleton - this means it cannot be redeclared anywhere else
del Config
