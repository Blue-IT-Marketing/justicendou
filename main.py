import datetime
from datetime import date
from typing import List, Union
import jinja2
# import firebase_admin
# from firebase_admin import credentials
# cred = credentials.Certificate('firebase/service_account.json')
# default_app = firebase_admin.initialize_app(cred)
from flask import Blueprint, make_response, render_template, url_for, request

from src.accounts import Accounts
from src.articles import Articles, default_topics, Interests
from src.services import HireMe
from utils.utils import date_string_to_date
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
    return render_template("justice-ndou/github.html")


def route_404():
    return render_template('404.html')


def route_500():
    return render_template('500.html')


def dashboard_handler():
    return render_template('dashboard/dashboard.html')


def route_login_post(route):
    # from firebase_admin import auth

    if route == "email-not-verified":
        return render_template('authentication/loggedin.html')

    elif route == "email-verified":
        return render_template('authentication/loggedin.html')

    elif route == "user-not-loggedin":
        return render_template('authentication/loggedout.html')

    elif route == "2":
        display_name = request.args.get('display_name')
        email = request.args.get('email')
        email_verified = request.args.get('email_verified')
        uid = request.args.get('uid')
        cell = request.args.get('cell')
        provider_data = request.args.get('provider_data')
        access_token = request.args.get('access_token')

        # decode_token = auth.verify_id_token(access_token)
        # uid = decode_token['uid']

        query = Accounts.query(Accounts.uid == uid)
        account_list = query.fetch()

        if account_list:
            account = account_list[0]
            account.write_email(email)

        else:
            query = Accounts.query(Accounts.email == email)
            account_list = query.fetch()
            if account_list:
                account = account_list[0]
                account.writeUserID(strinput=uid)
            else:
                account = Accounts()
                account.write_user_id(uid)
                account.write_names(display_name)
                account.write_email(email)
                account.write_provider_data(provider_data)

        if email_verified == "YES":
            account.write_verified(True)
        else:
            account.write_verified(False)
            account.write_user_id(uid)
            account.write_cell(cell)
            account.write_provider_data(provider_data)

        account.write_access_token(access_token)
        account.put()

        # TODO - Refine this part


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
            find_hires = HireMe.query(HireMe.project_status != "completed")
            this_hires_list = find_hires.fetch()
            return render_template('dashboard/hireme.html', this_hires_list=this_hires_list)

        elif "get-project" in route_list:  # dashboard project get
            project_id = request.args.get('project_id')
            find_hires = HireMe.query(HireMe.project_id == project_id)
            this_hires_list = find_hires.fetch()
            if this_hires_list:
                this_hire = this_hires_list[0]
                return render_template('dashboard/project.html', this_hire=this_hire)
            else:
                this_hire = HireMe()
                return render_template('dashboard/project.html', this_hire=this_hire)

        elif "update-project" in route_list:  # dashboard project updater
            cell, company, email, facebook, freelancing, names, project_description, project_id, project_status, \
            project_title, project_type, start_date, twitter, website = get_project_details()

            start_date = date_string_to_date(start_date)

            find_project = HireMe.query(HireMe.project_id == project_id)
            this_project_list = find_project.fetch()
            if this_project_list:
                this_project = this_project_list[0]
            else:
                this_project = HireMe()

            this_project.write_names(names=names)
            this_project.write_cell(cell=cell)
            this_project.write_email(email=email)
            this_project.write_website(website=website)
            this_project.write_facebook(facebook=facebook)
            this_project.write_twitter(twitter=twitter)
            this_project.write_company(company=company)
            this_project.write_freelancing(freelancing=freelancing)
            this_project.write_project_type(project_type=project_type)
            this_project.write_project_title(project_title=project_title)
            this_project.write_project_description(project_description=project_description)
            this_project.write_start_date(start_date=start_date)
            this_project.set_project_status(status=project_status)
            this_project.put()

            return "project successfully updated", 200

        elif "messages" in route_list:
            return render_template('dashboard/messages.html')

        elif "interests" in route_list:
            find_topics = Interests.query()
            interests_list = find_topics.fetch()
            return render_template('dashboard/interests.html', interests_list=interests_list)

        elif "createpage" in route_list:
            return render_template('dashboard/createpage.html')

        elif "createposts" in route_list:
            return render_template('dashboard/createposts.html')
        elif "subjectfromtopicid" in route_list:
            topic_id = request.args.get('topic_id')
            find_subjects = Interests.query(Interests.topic_id == topic_id)
            this_interests_list = find_subjects.fetch()
            if this_interests_list:
                this_interest = this_interests_list[0]
                # this_subjects_list = this_interest.subjects.split(this_interest._sep)
                # logging.info(this_subjects_list)
                return this_interest.subjects, 200

        elif "addsubjectstotopicid" in route_list:
            topic_id = request.args.get('topic_id')
            subjects_list = request.args.get('subjects-list')
            find_subjects = Interests.query(Interests.topic_id == topic_id)
            this_interests_list = find_subjects.fetch()
            if this_interests_list:
                this_interest = this_interests_list[0]
            else:
                this_interest = Interests()

            this_interest.write_topic_id(topic_id=topic_id)
            subjects_list = subjects_list.split(this_interest._sep)
            for subject in subjects_list:
                this_interest.write_subjects(subject=subject)

            this_interest.put()
            return "completed adding subjects", 200

        elif "removesubjectstopicid" in route_list:
            topic_id = request.args.get('topic_id')
            subjects_list = request.args.get('subjects-list')
            find_subjects = Interests.query(Interests.topic_id == topic_id)
            this_interests_list = find_subjects.fetch()
            if this_interests_list:
                this_interest = this_interests_list[0]
                temp_subjects_list = this_interest.subjects.split(this_interest.sep)
                subjects_list = subjects_list.split(":")
                for subject in subjects_list:
                    if subject in temp_subjects_list:
                        temp_subjects_list.remove(subject)
                this_interest.subjects = ""
                for subject in temp_subjects_list:
                    if this_interest.subjects == "":
                        this_interest.subjects = subject
                    else:
                        this_interest.subjects += ':' + subject

                this_interest.put()
                return "subjects removed", 200

        elif "createtopic" in route_list:
            topic_id = request.args.get('topic_id')
            topic_label = request.args.get('topic_label')
            find_topic = Interests.query(Interests.topic == topic_label)
            default_topics_list = find_topic.fetch()

            if len(default_topics_list) > 0:
                return "This topic is already present", 200
            else:
                this_interest = Interests()
                this_interest.write_topic_id(topic_id=topic_id)
                this_interest.write_topic(topic=topic_label)
                this_interest.put()
                return "Topic successfully created", 200

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
        elif 'gtihub-profile':
            return route_github_profile()

        elif "500" in route_list:
            return route_500()
        else:
            return route_home()


def get_project_details():
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
