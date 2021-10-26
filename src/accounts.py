import os
import string
from random import choices

import jinja2
from google.cloud import ndb
import datetime

from google.cloud.ndb.exceptions import BadValueError

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
