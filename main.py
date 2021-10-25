from typing import List

# import firebase_admin
# from firebase_admin import credentials
# cred = credentials.Certificate('firebase/service_account.json')
# default_app = firebase_admin.initialize_app(cred)
from flask import Blueprint, make_response, render_template, request, jsonify
from google.cloud import ndb

from src.accounts import Accounts
from src.articles import Articles, Interests
from src.exception_handlers import handle_view_errors
from src.exceptions import status_codes, InputError, DataServiceError
from src.services import HireMe
from src.use_context import use_context
from utils.utils import date_string_to_date, create_id

main_router_bp = Blueprint('main_router_handler', __name__)


def route_sitemap():
    # TODO- Consider creating a dynamic sitemap by actually crawling my site and then outputting the sitemap here
    # TODO- i think i use to have a function to do this coupled with thoth
    response = make_response(render_template('sitemap/sitemap.xml'))
    response.headers["Content-Type"] = 'text/xml'
    return response, 200


def route_robots():
    """
    """
    response = make_response(render_template('sitemap/robots.txt'))
    response.headers["Content-Type"] = "text/plain"
    return response, 200


def route_home():
    articles = Articles.fetch_random_articles()
    print(f'articles : {articles}')
    context = dict(title='Justice Ndou Software Development Profile Web Application',
                   description='Justice Ndou is a web application developer, experienced in python and node.js back '
                               'end development and also develops REST API''s i am also available to work on '
                               'freelance projects')
    if articles:
        articles = articles['articles']
        context.update(articles=articles)
        return render_template('index.html', **context), 200

    return render_template('index.html', **context), 200


def route_login():
    context = dict(title='Justice Ndou Profile | Admin Login',
                   description='Admin only Login Page for Justice Ndou Profile Web Application')
    return render_template('authentication/login.html', **context), 200


def route_logout():
    context = dict(title='Justice Ndou Profile | Admin Logout',
                   description='Admin only Logout Page for Justice Ndou Profile Web Application')
    return render_template('authentication/logout.html', **context), 200


def route_about():
    context = dict(title='Justice Ndou Profile | About Page',
                   description='About Justice Ndou - More information on who is Justice Ndou, '
                               'what he does and he is busy with at the moment')
    return render_template('about.html', **context), 200


def route_contact():
    context = dict(title='Justice Ndou Profile | Contact Page',
                   description='Contact Justice Ndou for web development purposes, '
                               'through our contact form social media accounts, cell or email address')
    return render_template('contact/contact.html', **context), 200


def route_dashboard():
    """ get correct user details"""
    # TODO add authentication for dashboard then display dashboard
    context = dict(title='Justice Ndou Profile | Dashboard Page',
                   description='Contacting Justice Ndou',
                   login_url='/login')
    return render_template("lockscreen.html", **context), 200


def route_github_profile():
    # TODO - load github page here through github version api
    context = dict(title='Justice Ndou Github Profile Page',
                   description='Justice Ndou Personal Github Profile, and also Open Source Projects i am '
                               'currently busy with')
    return render_template("justice-ndou/github.html", **context), 200


def route_404():
    context = dict(title="Justice Ndou Profile : 404 Error Page",
                   description="Unfortunately the Page you are looking for was not found")
    return render_template('404.html', **context), 404


def route_500():
    context = dict(title="Justice Ndou Profile : 500 Error Page",
                   description="General Server Error")
    return render_template('500.html', **context), 500


def dashboard_handler():
    context = dict(title="Justice Ndou Profile | Dashboard Page",
                   description="Admin Only Dashboard Page if you are not Me or haven't Hired Me as a freelancer "
                               "then dont visit this page")
    return render_template('dashboard/dashboard.html', **context), 200


def route_login_post(route):
    # from firebase_admin import auth

    if route == "email-not-verified":
        return render_template('authentication/loggedin.html')

    elif route == "email-verified":
        return render_template('authentication/loggedin.html')

    elif route == "user-not-loggedin":
        return render_template('authentication/loggedout.html')

    elif route == "2":
        access_token, cell, display_name, email, email_verified, provider_data, uid = get_user_args()
        # decode_token = auth.verify_id_token(access_token)
        # uid = decode_token['uid']
        return update_or_create_account(access_token, cell, display_name, email, email_verified, provider_data, uid)

        # TODO - Refine this part


@use_context
@handle_view_errors
def update_or_create_account(access_token, cell, display_name, email, email_verified, provider_data, uid) -> tuple:
    """
    **update_or_create_account**
        update an existing user account or create a new one
    """
    account = Accounts.query(Accounts.uid == uid).get()
    if not isinstance(account, Accounts) or not account.uid:
        account = Accounts()
        account.uid = uid
        account.email = email
    account.access_token = access_token
    account.cell = cell
    account.names = display_name
    account.email_verified = email_verified
    account.provider_data = provider_data
    key: ndb.Key = account.put()
    if not isinstance(key, ndb.Key):
        raise DataServiceError(description='unable to create or update account')
    return jsonify(status=True, payload=account.to_dict(), message='Account successfully created')


def get_user_args():
    """ **get_user_args** fetches user arguments from arguments"""
    display_name = request.args.get('display_name')
    email = request.args.get('email')
    email_verified = request.args.get('email_verified')
    uid = request.args.get('uid')
    cell = request.args.get('cell')
    provider_data = request.args.get('provider_data')
    access_token = request.args.get('access_token')
    return access_token, cell, display_name, email, email_verified, provider_data, uid


def get_route_list(path: str) -> List[str]: return path.lower().split("/")


def is_login_route(route: List[str]) -> bool:
    """

    :param route:
    :return:
    """
    return "login" in route or "login.html" in route or "signin" in route or "signin.html" in route or "subscribe" \
           in route or "subscribe.html" in route


@main_router_bp.route('/<string:path>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def main_router_handler(path: str):
    route_list: List[str] = get_route_list(path=path)
    if request.method == 'POST':
        if "hireme" in route_list:
            this_hires_list = get_completed_projects()
            return render_template('dashboard/hireme.html', this_hires_list=this_hires_list)

        elif "get-project" in route_list:  # dashboard project get
            this_hire = get_project_details()
            return render_template('dashboard/project.html', this_hire=this_hire.to_dict())

        elif "update-project" in route_list:  # dashboard project updater
            project_key, project_instance = create_update_project()
            if isinstance(project_key, ndb.Key):
                return jsonify(dict(status=True,
                                    payload=dict(project_key=project_key, project_instance=project_instance.to_dict()),
                                    message='successfully updated project')), status_codes.successfully_updated_code
            _message: str = 'project not found: unable to update project'
            return jsonify(dict(status=False,
                                message=_message)), status_codes.data_not_found_code

        elif "messages" in route_list:
            return render_template('dashboard/messages.html')

        elif "interests" in route_list:
            interests_list = [interest.to_dict() for interest in get_articles_interests()]
            return render_template('dashboard/interests.html', interests_list=interests_list)

        elif "create-page" in route_list:
            return render_template('dashboard/createpage.html')

        elif "create-posts" in route_list:
            return render_template('dashboard/createposts.html')

        elif "subjects-from-topic" in route_list:
            topic_id = request.args.get('topic_id')
            _interests = [interest.to_dict() for interest in get_articles_interests() if interest.topic_id == topic_id]
            return jsonify(dict(status=True,
                                payload=_interests,
                                message='')), 200

        elif "add-subjects-to-topic" in route_list:
            return dict(status=True,
                        payload=add_subjects_to_topics().to_dict(),
                        message='subjects successfully updated on topic'), status_codes.successfully_updated_code

        elif "remove-subjects-from-topics" in route_list:
            return remove_subject_from_topic()

        elif "create-topic" in route_list:
            return create_topic()

        elif is_login_route(route=route_list):
            _route = request.args.get("route_list")
            return route_login_post(route=_route)

        elif "dashboard" in route_list:
            _route = request.args.get('route_list')
            return route_dashboard()

    elif request.method == 'GET':
        if "index" in route_list or "index.html" in route_list:
            return route_home()
        elif is_login_route(route=route_list):
            return route_login()

        elif "logout" in route_list or "logout.html" in route_list or "signout" in route_list or \
                "signout.html" in route_list:
            return route_logout()

        elif "sitemap.xml" in route_list:
            return route_sitemap()

        elif "robots.txt" in route_list:
            return route_robots()

        elif "about" in route_list or "about.html" in route_list:
            return route_about()

        elif "contact" in route_list or "contact.html" in route_list:
            return route_contact()

        elif "dashboard" in route_list or "dashboard.html" in route_list:
            return route_dashboard()
        elif 'github-profile' in route_list:
            return route_github_profile()
        elif "500" in route_list:
            return route_500()
        else:
            return route_home()


@use_context
@handle_view_errors
def create_topic():
    topic = request.args.get('topic')
    topic_instance = Interests.query(Interests.topic == topic.lower().strip()).get()
    if isinstance(topic_instance, Interests):
        return jsonify(dict(status=False, message='topic already present')), status_codes.status_ok_code

    this_interest = Interests()
    this_interest.topic_id = create_id()
    this_interest.topic = topic
    this_interest.put()
    return jsonify(dict(status=True,
                        payload=this_interest.to_dict(),
                        message='successfully created topic')), status_codes.successfully_updated_code


@use_context
@handle_view_errors
def remove_subject_from_topic():
    topic_id = request.args.get('topic_id')
    subject = request.args.get('subject')
    _interest = Interests.query(Interests.topic_id == topic_id).fetch()
    if not (isinstance(_interest, Interests) and Interests.topic_id):
        return jsonify(dict(status=False, message='topic not found')), status_codes.data_not_found_code
    _subjects_list = _interest.subjects.split(Interests().sep)
    _interest.subjects = f"{Interests.sep}".join([_subject for _subject in _subjects_list
                                                  if subject not in _interest.subjects.split(Interests().sep)])
    key: ndb.Key = _interest.put()
    if not isinstance(key, ndb.Key):
        raise DataServiceError(description='Database Error: unable to update database')
    return jsonify(status=True,
                   payload=_interest.to_dict(),
                   message='subject successfully removed'), status_codes.successfully_updated_code


@use_context
@handle_view_errors
def add_subjects_to_topics() -> Interests:
    # TODO insure that data is being passed in JSON format
    topic_id = request.args.get('topic_id')
    subjects_list = request.args.get('subjects-list')
    if not topic_id:
        raise InputError(description='topic_id is required')

    this_interest = Interests.query(Interests.topic_id == topic_id).get()
    if not isinstance(this_interest, Interests) and Interests.topic_id:
        return jsonify(dict(status=False, message='error: topic not found'))
    this_interest.subjects = subjects_list
    this_interest.put()
    return this_interest


@use_context
@handle_view_errors
def get_articles_interests() -> List[Interests]:
    return Interests.query().fetch()


@use_context
@handle_view_errors
def get_completed_projects() -> List[HireMe]:
    return HireMe.query(HireMe.project_status != "completed").fetch()


@use_context
@handle_view_errors
def get_project_details() -> HireMe:
    project_id = request.args.get('project_id')
    this_hire = HireMe.query(HireMe.project_id == project_id).get()
    return HireMe.query(HireMe.project_id == project_id).get()


@use_context
@handle_view_errors
def create_update_project() -> tuple:
    (cell, company, email, facebook, freelancing, names, project_description, project_id, project_status,
     project_title, project_type, start_date, twitter, website) = get_project_arg_details()
    start_date = date_string_to_date(start_date)
    this_project = HireMe.query(HireMe.project_id == project_id).get()
    if not isinstance(this_project, HireMe) and HireMe.project_id:
        this_project = HireMe()
        this_project.project_id = create_id()
    this_project.names = names
    this_project.cell = cell
    this_project.email = email
    this_project.website = website
    this_project.facebook = facebook
    this_project.twitter = twitter
    this_project.company = company
    this_project.freelancing = freelancing
    this_project.project_type = project_type
    this_project.project_title = project_title
    this_project.project_description = project_description
    this_project.start_date = start_date
    this_project.project_status = project_status
    return this_project.put(), this_project.to_dict()


def get_project_arg_details():
    project_id = request.args.get('project_id')
    names = request.args.get('names')
    cell = request.args.get('cell')
    email = request.args.get('email')
    website = request.args.get('website')
    facebook = request.args.get('facebook')
    twitter = request.args.get('twitter')
    company = request.args.get('company')
    freelancing = request.args.get('freelancing')
    project_type = request.args.get('project-type')
    project_title = request.args.get('project-title')
    project_description = request.args.get('project-description')
    estimated_budget = request.args.get('estimated-budget')
    start_date = request.args.get('start-date')
    project_status = request.args.get('project-status')
    return (cell, company, email, facebook, freelancing, names, project_description, project_id, project_status,
            project_title, project_type, start_date, twitter, website)


@main_router_bp.route('/', methods=['GET'])
def home_router():
    return route_home()
