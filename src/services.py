import datetime
import os
import jinja2
from flask import Blueprint, request
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadValueError

from src.exceptions import InputError

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

services_handler_bp = Blueprint('services_handler', __name__)


class ProjectMessages(ndb.Model):
    """
        ** Class ProjectMessages **
            messages relating to projects
    """
    project_id = ndb.StringProperty()
    subject = ndb.StringProperty()
    message = ndb.StringProperty()
    message_type = ndb.StringProperty(default="email")  # sms
    date_sent = ndb.DateProperty(auto_now_add=True)
    time_sent = ndb.TimeProperty(auto_now_add=True)
    response = ndb.StringProperty(default=None)
    date_responded = ndb.DateProperty(auto_now=True)
    time_responded = ndb.TimeProperty(auto_now=True)

    @property
    def response_sent(self) -> bool:
        return bool(self.response)

    def write_project_id(self, projectid):
        self.project_id = projectid

    def write_subject(self, subject):
        self.subject = subject

    def write_message(self, message):
        self.message = message

    def write_message_type(self, message_type):
        try:
            if message_type in ['sms', 'email']:
                self.message_type = message_type
        except BadValueError as e:
            raise e

    def write_date_sent(self, date_sent):
        if isinstance(date_sent, datetime.date):
            self.date_sent = date_sent
        else:
            raise BadValueError()

    def write_time_sent(self, time_sent):
        if isinstance(time_sent, datetime.time):
            self.time_sent = time_sent
        else:
            raise BadValueError()

    def write_response(self, response):
        self.response = response

    def write_date_response_sent(self, date_response):
        if isinstance(datetime.date, date_response):
            self.date_responded = date_response
        else:
            raise BadValueError()

    def write_time_response_sent(self, time_response):
        if isinstance(datetime.time, time_response):
            self.time_responded = time_response
            return True
        else:
            raise BadValueError()


class HireMe(ndb.Model):
    uid = ndb.StringProperty()
    project_id = ndb.StringProperty()
    names = ndb.StringProperty()
    cell = ndb.StringProperty()
    email = ndb.StringProperty()
    website = ndb.StringProperty()
    facebook = ndb.StringProperty()
    twitter = ndb.StringProperty()
    company = ndb.StringProperty()
    freelancing = ndb.StringProperty()
    project_type = ndb.StringProperty()
    project_title = ndb.StringProperty()
    project_description = ndb.StringProperty()
    estimated_budget = ndb.IntegerProperty(default=50)
    start_date = ndb.DateProperty(auto_now_add=True)
    project_status = ndb.StringProperty(default="created")  # read, started, milestone, completed

    def send_email(self, message):
        """
            given an email message send to project owner
        """
        pass

    def send_sms(self, sms):
        """
         give an sms message send to project owner
        """
        pass


@services_handler_bp.route('/services', methods=['GET', 'POST'])
def services_handler():
    route = request.args.get('route')
    if route == "hireme":
        args = dict(get_hireme_args())
        return "Successfully created your project with project code : " + create_hireme_model(args).project_id

    elif route == "get-hireme-requests":
        this_find_requests = HireMe.query(HireMe.project_status != "completed")
        this_hireme_list = this_find_requests.fetch()

        template = template_env.get_template("justice-ndou/personal-profile/services/hireme-list.html")
        return template.render(dict(thishiremelist=this_hireme_list))


def get_hireme_args():
    """
        **get_hireme_args**

        :return:
    """
    names = request.args.get('names')
    if not names:
        raise InputError(description='names cannot be Null')
    cell = request.args.get('cell')
    if not cell:
        raise InputError(description='Cell cannot be Null')
    email = request.args.get('email')
    if not email:
        raise InputError(description='Email cannot be Null')

    website = request.args.get('website')
    if not website:
        raise InputError(description='Website cannot be Null')

    facebook = request.args.get('myfacebook')
    if not facebook:
        raise InputError(description='Facebook cannot be Null')
    twitter = request.args.get('mytwitter')
    if not twitter:
        raise InputError(description='Twitter cannot be Null')

    company = request.args.get('company')
    if not company:
        raise InputError(description='Company cannot be Null')

    freelancing = request.args.get('freelancing')
    if not freelancing:
        raise InputError(description='Freelancing cannot be Null')

    project_type = request.args.get('projecttype')
    if not project_type:
        raise InputError(description='project type cannot be Null')

    project_title = request.args.get('projecttitle')
    if not project_title:
        raise InputError(description='Project Title cannot be Null')

    project_description = request.args.get('projectdescription')
    if not project_description:
        raise InputError(description='ProjectDescription cannot be Null')

    return cell, company, email, facebook, freelancing, names, project_description, project_title, \
           project_type, twitter, website


def create_hireme_model(args):
    """
        **create_hireme_mnodel**

    """

    this_hire_me = HireMe()
    this_hire_me.names = args.get('names')
    this_hire_me.cell = args.get('cell')
    this_hire_me.email = args.get('email')
    this_hire_me.website = args.get('website')
    this_hire_me.facebook = args.get('facebook')
    this_hire_me.twitter = args.get('twitter')
    this_hire_me.company = args.get('company')
    this_hire_me.freelancing = args.get('freelancing')
    this_hire_me.project_type = args.get('project_type')
    this_hire_me.project_title = args.get('project_title')
    this_hire_me.project_description = args.get('project_description')
    key = this_hire_me.put()
    return this_hire_me


@services_handler_bp.route('/services/<string:path>', methods=['POST', 'GET'])
def this_services_handler(path: str):
    if request.method == "GET":
        """
            Note get the uid from the firebase script on the user end and then use that as a uid
        """
        do_hire_template = template_env.get_template("justice-ndou/personal-profile/services/dohire.html")
        status_template = template_env.get_template("justice-ndou/personal-profile/services/status.html")
        # NOTE this will return the correct template depending on path
        return dict(dohire=do_hire_template,
                    request_status=status_template).get(path.replace("-", "_")).render(dict()), 200

    elif request.method == "POST":
        route = request.args.get('route')

        if route == "request-this-status":
            project_id = request.args.get('project_id')
            this_project = HireMe.query(HireMe.project_id == project_id).get()
            if not isinstance(this_project, HireMe) or not bool(this_project.project_id):
                this_project = HireMe()
            template = template_env.get_template('justice-ndou/personal-profile/services/status-response.html')
            return template.render(dict(thisproject=this_project.to_dict())), 200
