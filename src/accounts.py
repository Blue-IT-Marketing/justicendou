import os

import jinja2
from google.cloud import ndb

from config import config_instance

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))


class Accounts(ndb.Expando):
    """
        ** Class Accounts **
            class controlling user information and access
    """
    uid = ndb.StringProperty()
    organization_id = ndb.StringProperty()
    names = ndb.StringProperty()
    surname = ndb.StringProperty()
    cell = ndb.StringProperty()
    tel = ndb.StringProperty()
    email = ndb.StringProperty()
    website = ndb.StringProperty()
    verified = ndb.BooleanProperty(default=False)
    verification_code = ndb.StringProperty()
    suspended = ndb.BooleanProperty(default=False)

    photo_url = ndb.StringProperty()
    provider_data = ndb.StringProperty()
    access_token = ndb.StringProperty()

    last_sign_in_date = ndb.DateProperty()
    last_sign_in_time = ndb.TimeProperty()
    timestamp = ndb.DateTimeProperty()

    @property
    def is_admin(self) -> bool:
        """
            **is_admin**
                will be true if user is admin
        :return:
        """
        return self.uid == config_instance.ADMIN_UID and not self.suspended

    @property
    def user_details(self) -> dict:
        return dict(names=self.names, surname=self.surname, cell=self.cell, tel=self.tel,
                    email=self.email, website=self.website)

    def verify_code(self, code: str) -> bool:
        """
            **verify_code**
                verifies verification and returns the result
                also has a side effect of modifying the verified property
        :param code:
        :return:
        """
        self.verified = self.verification_code == code
        return self.verified

    def __bool__(self) -> bool:
        return bool(self.uid)

    def __str__(self) -> str:
        return f"{self.user_details}"
