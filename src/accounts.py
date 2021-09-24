import os
import string
from random import choices

import jinja2
from google.cloud import ndb
import datetime

from google.cloud.ndb.exceptions import BadValueError

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))


class Accounts(ndb.Expando):
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

    def write_last_sign_in_date(self, in_date: datetime.date) -> bool:
        try:
            if isinstance(in_date, datetime.date):
                self.last_sign_in_date = in_date
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_last_sign_in_time(self, in_time: datetime.time):
        try:
            if isinstance(in_time, datetime.time):
                self.last_sign_in_time = in_time
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_photo_url(self, photo_url: str):
        try:

            if photo_url is not None:
                self.photo_url = photo_url
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_provider_data(self, provider_data: str):
        try:
            if provider_data is not None:
                self.provider_data = provider_data
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_access_token(self, access_token: str):
        try:
            if access_token is not None:
                self.access_token = access_token
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_verified(self, is_verified: bool):
        try:
            if isinstance(is_verified, bool):
                self.verified = is_verified
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_verification_code(self, verification_code: str):
        try:
            if verification_code is not None:
                self.verification_code = verification_code
                return True
            else:
                return False
        except BadValueError:
            return False

    @staticmethod
    def create_verification_code():
        return ''.join(choices(string.digits + string.ascii_uppercase, k=6))

    def write_user_id(self, uid: str):
        try:
            if uid is not None:
                self.uid = uid
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_organization_id(self, organization_id: str):
        try:
            if organization_id is not None:
                self.organization_id = organization_id
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_names(self, names: str):
        try:
            if names is not None:
                self.names = names
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_surname(self, surname: str):
        try:
            if surname is not None:
                self.surname = surname
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_cell(self, cell: str):
        # this is just to test git
        try:
            if cell is not None:
                self.cell = cell
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_tel(self, tel: str):
        try:
            if tel is not None:
                self.tel = tel
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_email(self, email: str):
        try:
            if email is not None:
                self.email = email
                return True
            else:
                return False
        except BadValueError:
            return False

    def write_website(self, website: str):
        try:
            if website is not None:
                self.website = website
                return True
            else:
                return False
        except BadValueError:
            return False
