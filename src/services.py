import logging
import os
import random
import string

import jinja2
import datetime

from flask import Blueprint, request
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadValueError

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

services_handler_bp = Blueprint('services_handler', __name__)


class ProjectMessages(ndb.Model):
    project_id = ndb.StringProperty()
    subject = ndb.StringProperty()
    message = ndb.StringProperty()
    message_type = ndb.StringProperty(default="email")  # sms
    date_sent = ndb.DateProperty(auto_now_add=True)
    time_sent = ndb.TimeProperty(auto_now_add=True)
    response = ndb.StringProperty()
    date_responded = ndb.DateProperty()
    time_responded = ndb.TimeProperty()

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

    def write_estimated_budget(self, estimated_budget):
        estimated_budget = str(estimated_budget)
        if estimated_budget.isdigit() and int(estimated_budget) > 0:
            self.estimated_budget = int(estimated_budget)
        else:
            raise BadValueError()

    def write_start_date(self, start_date):
        if isinstance(start_date, datetime.date):
            self.start_date = start_date
            return True
        else:
            raise BadValueError()

    def set_project_status(self, status):
        status = str(status)
        if status in ["created", "read", "started", "milestone", "completed"]:
            self.project_status = status
            return True
        else:
            return False

    def write_project_id(self, project_id):
        self.project_id = project_id

    @staticmethod
    def create_id():
        return "".join(random.choices(string.digits + string.ascii_uppercase, k=64))

    def write_userid(self, uid: str):
        self.uid = uid

    def write_names(self, names):
        self.names = names.strip().lower()

    def write_cell(self, cell):
        self.cell = cell

    def write_email(self, email):
        self.email = email

    def write_website(self, website):
        self.website = website

    def write_facebook(self, facebook):
        self.facebook = facebook

    def write_twitter(self, twitter):
        self.twitter = twitter

    def write_company(self, company):
        self.company = company

    def write_freelancing(self, freelancing):
        self.freelancing = freelancing

    def write_project_type(self, project_type):
        self.project_type = project_type

    def write_project_title(self, project_title):
        self.project_title = project_title

    def write_project_description(self, project_description):
        self.project_description = project_description


@services_handler_bp.route('/services', methods=['GET', 'POST'])
def services_handler():
    route = request.args.get('route')
    if route == "hireme":
        names = request.args.get('names')
        cell = request.args.get('cell')
        email = request.args.get('email')
        website = request.args.get('website')
        facebook = request.args.get('myfacebook')
        twitter = request.args.get('mytwitter')
        company = request.args.get('company')
        freelancing = request.args.get('freelancing')
        project_type = request.args.get('projecttype')
        project_title = request.args.get('projecttitle')
        project_description = request.args.get('projectdescription')

        logging.info("services handler received all variables")

        # //TODO- please do error corrections within the browser using javascript

        this_hire_me = HireMe()

        if not this_hire_me.write_names(names=names):
            return "Please enter correct Names"
        elif not this_hire_me.write_cell(cell=cell):
            return "Please enter a valid cell phone Number"
        elif not this_hire_me.write_email(email=email):
            return "Please enter a valid email address"
        elif not this_hire_me.write_website(website=website):
            return "Please enter a valid website address"
        elif not this_hire_me.write_company(company=company):
            return "Please enter a valid company name"
        elif not this_hire_me.write_project_type(project_type=project_type):
            return "Please enter a valid project type"
        elif not this_hire_me.write_project_title(project_title=project_title):
            return "Please enter a valid project title"
        elif not this_hire_me.write_project_description(project_description=project_description):
            return "Please enter a valid project description"

        else:
            this_hire_me.write_facebook(facebook=facebook)
            this_hire_me.write_twitter(twitter=twitter)
            this_hire_me.write_freelancing(freelancing=freelancing)
            this_hire_me.write_project_id(project_id=this_hire_me.create_id())
            this_hire_me.put()

            return "Successfully created your project with project code : " + this_hire_me.project_id

    elif route == "get-hireme-requests":

        this_find_requests = HireMe.query(HireMe.project_status != "completed")
        this_hireme_list = this_find_requests.fetch()

        template = template_env.get_template(
            "justice-ndou/personal-profile/services/hireme-list.html")
        context = {'thishiremelist': this_hireme_list}
        return template.render(context)


@services_handler_bp.route('/services/<string:path>', methods=['POST', 'GET'])
def this_services_handler(path: str):
    if request.method == "GET":
        """
            Note get the uid from the firebase script on the user end and then use that as a uid
        """
        # TODO- just show the hireme form
        if path == "dohire":
            template = template_env.get_template("justice-ndou/personal-profile/services/dohire.html")
            context = {}
            return template.render(context), 200

        elif path == "request-status":
            template = template_env.get_template("justice-ndou/personal-profile/services/status.html")
            context = {}
            return template.render(context), 200

    elif request.method == "POST":
        route = request.args.get('route')

        if route == "request-this-status":
            project_id = request.args.get('project_id')
            this_project_query = HireMe.query(HireMe.project_id == project_id)
            this_project_list = this_project_query.fetch()

            if this_project_list:
                this_project = this_project_list[0]

                template = template_env.get_template(
                    'justice-ndou/personal-profile/services/status-response.html')
                context = {'thisproject': this_project}
                return template.render(context), 200
            else:
                this_project = HireMe()
                template = template_env.get_template(
                    'justice-ndou/personal-profile/services/status-response.html')
                context = {'thisproject': this_project}
                return template.render(context), 200
