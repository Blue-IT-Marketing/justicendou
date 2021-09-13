import os
import jinja2
from google.cloud import ndb
import datetime

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

    def write_last_sign_in_date(self, strinput):
        try:
            if isinstance(strinput, datetime.date):
                self.last_sign_in_date = strinput
                return True
            else:
                return False
        except:
            return False

    def write_last_sign_in_time(self, strinput):
        try:
            if isinstance(strinput, datetime.time):
                self.last_sign_in_time = strinput
                return True
            else:
                return False
        except:
            return False

    def write_photo_url(self, strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.photo_url = strinput
                return True
            else:
                return False
        except:
            return False

    def write_provider_data(self, strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.provider_data = strinput
                return True
            else:
                return False
        except:
            return False

    def write_access_token(self, strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.access_token = strinput
                return True
            else:
                return False
        except:
            return False

    def write_verified(self, strinput):
        try:
            if strinput in [True, False]:
                self.verified = strinput
                return True
            else:
                return False

        except:
            return False

    def write_verification_code(self, strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.verification_code = strinput
                return True
            else:
                return False
        except:
            return False

    def create_verification_code(self):
        import random, string
        try:
            strVerificationCode = ""
            for i in range(6):
                strVerificationCode += random.SystemRandom().choice(string.digits + string.ascii_uppercase)
            return strVerificationCode
        except:
            return None

    def write_user_id(self, strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.uid = strinput
                return True
            else:
                return False
        except:
            return False

    def writeOrganizationID(self, strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.organization_id = strinput
                return True
            else:
                return False
        except:
            return False

    def writeNames(self, strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.names = strinput
                return True
            else:
                return False
        except:
            return False

    def writeSurname(self, strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.surname = strinput
                return True
            else:
                return False
        except:
            return False

    def writeCell(self, strinput):
        # this is just to test git
        try:
            strinput = str(strinput)
            if strinput != None:
                self.cell = strinput
                return True
            else:
                return False
        except:
            return False

    def writeTel(self, strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.tel = strinput
                return True
            else:
                return False
        except:
            return False

    def writeEmail(self, strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.email = strinput
                return True
            else:
                return False
        except:
            return False

    def writeWebsite(self, strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.website = strinput
                return True
            else:
                return False
        except:
            return False
