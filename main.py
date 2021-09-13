import datetime
from typing import List

# import firebase_admin
# from firebase_admin import credentials
# cred = credentials.Certificate('templates/firebase/service_account.json')
# default_app = firebase_admin.initialize_app(cred)
from flask import Blueprint, make_response, render_template, url_for, request

from src.accounts import Accounts
from src.articles import Articles, this_topics, Interests
from src.services import HireMe

main_router_bp = Blueprint('main_router_handler', __name__)


def route_sitemap(self):
    # TODO- Consider creating a dynamic sitemap by actually crawling my site and then outputting the sitemap here
    # TODO- i think i use to have a function to do this coupled with thoth
    response = make_response(render_template('templates/sitemap/sitemap.xml'))
    response.headers["Content-Type"] = 'text/xml'
    return response, 200


def route_robots():
    response = make_response(render_template('templates/sitemap/robots.txt'))
    response.headers["Content-Type"] = "text/plain"
    return response, 200


def route_home():
    import random
    this_articles = Articles()
    # this_articles.save_topics()

    topic = random.choice(this_topics)
    articles = this_articles.fetch_topic(topic=topic)

    if articles != "":
        articles = articles['articles']
    return render_template('templates/index.html', articles=articles), 200


def route_login():
    return render_template('templates/authentication/login.html'), 200


def route_logout():
    return render_template('templates/authentication/logout.html'), 200


def route_about():
    return render_template('templates/about.html'), 200


def route_contact():
    return render_template('templates/contact/contact.html')


def route_blog():
    return render_template("templates/blog/home.html")


def route_algorithms():
    return render_template("templates/algorithms/algos.html")


def route_strange():
    return render_template("templates/algorithms/strange/strange.html")


def route_perlin():
    return render_template("templates/algorithms/perlin/perlin.html")


def route_life():
    return render_template("templates/algorithms/gameoflife/life.html")


def route_maze():
    return render_template("templates/algorithms/maze/maze.html")


def route_path():
    return render_template("templates/algorithms/pathfinder/path.html")


def route_matter():
    return render_template("templates/algorithms/matter/matter.html")


def route_dashboard():
    """ get correct user details"""
    user = Accounts()
    if user.is_current_user_admin():
        # Update this Note:
        logout_url = url_for('user_logout')
        return render_template("templates/dashboard/dashboard.html", logout_url=logout_url)
    else:
        login_url = url_for('login_url')
        return render_template("templates/lockscreen.html", login_url=login_url)


def route_games():
    return render_template("templates/games/games.html")


def route_tetris():
    return render_template("templates/games/tetris/tetris.html")


def route_pacman():
    return render_template("templates/games/pacman/pacman.html")


def route_chess():
    return render_template("templates/games/garbo/chess.html")


def route_checkers():
    return render_template("templates/games/checkers/checkers.html")


def route_ping_pong():
    return render_template("templates/games/pingpong/pingpong.html")


def route_matrix():
    return render_template("templates/games/matrix/matrix.html")


def route_snake():
    return render_template("templates/games/snake/snake.html")


def route_plinko():
    return render_template("templates/algorithms/plinko/plinko.html")


def route_maze_solver():
    return render_template("templates/algorithms/mazepath/mazepath.html")


def route_404():
    return render_template('templates/404.html')


def route_500():
    return render_template('templates/500.html')


def date_string_datetime(date_string):
    try:
        date_string = str(date_string)
        try:
            date_list = date_string.split("\\")
            my_year = int(date_list[0])
            my_month = int(date_list[1])
            my_day = int(date_list[2])
        except:
            date_list = date_string.split("-")

            if len(date_list) == 3:
                my_year = int(date_list[0])
                my_month = int(date_list[1])
                my_day = int(date_list[2])
            else:
                this_date = datetime.datetime.now()
                this_date = this_date.date()
                my_year = this_date.year
                my_month = this_date.month
                my_day = this_date.day

        this_date = datetime.date(year=my_year, month=my_month, day=my_day)

        return this_date


    except Exception as e:
        raise e


def dashboard_handler():
    return render_template('templates/dashboard/dashboard.html')


def route_login_post(route):
    # from firebase_admin import auth

    if route == "email-not-verified":
        return render_template('templates/authentication/loggedin.html')

    elif route == "email-verified":
        return render_template('templates/authentication/loggedin.html')

    elif route == "user-not-loggedin":
        return render_template('templates/authentication/loggedout.html')

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
            account.writeEmail(email)

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
            return render_template('templates/dashboard/hireme.html', this_hires_list=this_hires_list)

        elif "get-project" in route_list:  # dashboard project get
            project_id = request.args.get('project_id')
            find_hires = HireMe.query(HireMe.projectid == project_id)
            this_hires_list = find_hires.fetch()
            if this_hires_list:
                this_hire = this_hires_list[0]
                return render_template('templates/dashboard/project.html', this_hire=this_hire)
            else:
                this_hire = HireMe()
                return render_template('templates/dashboard/project.html', this_hire=this_hire)

        elif "update-project" in route_list:  # dashboard project updater
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

            start_date = date_string_datetime(start_date)

            find_project = HireMe.query(HireMe.projectid == project_id)
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
            return render_template('templates/dashboard/messages.html')

        elif "interests" in route_list:
            find_topics = Interests.query()
            interests_list = find_topics.fetch()
            return render_template('templates/dashboard/interests.html', interests_list=interests_list)

        elif "createpage" in route_list:
            return render_template('templates/dashboard/createpage.html')

        elif "createposts" in route_list:
            return render_template('templates/dashboard/createposts.html')
        elif "subjectfromtopicid" in route_list:
            topicid = request.args.get('topicid')
            find_subjects = Interests.query(Interests.topic_id == topicid)
            this_interests_list = find_subjects.fetch()
            if this_interests_list:
                this_interest = this_interests_list[0]
                # this_subjects_list = this_interest.subjects.split(this_interest._sep)
                # logging.info(this_subjects_list)
                return this_interest.subjects, 200

        elif "addsubjectstotopicid" in route_list:
            topicid = request.args.get('topicid')
            subjects_list = request.args.get('subjects-list')
            find_subjects = Interests.query(Interests.topic_id == topicid)
            this_interests_list = find_subjects.fetch()
            if this_interests_list:
                this_interest = this_interests_list[0]
            else:
                this_interest = Interests()

            this_interest.write_topic_id(id=topicid)
            subjects_list = subjects_list.split(this_interest._sep)
            for subject in subjects_list:
                this_interest.write_subjects(subject=subject)

            this_interest.put()
            return "completed adding subjects", 200

        elif "removesubjectstopicid" in route_list:
            topicid = request.args.get('topicid')
            subjects_list = request.args.get('subjects-list')
            find_subjects = Interests.query(Interests.topic_id == topicid)
            this_interests_list = find_subjects.fetch()
            if this_interests_list:
                this_interest = this_interests_list[0]
                temp_subjects_list = this_interest.subjects.split(this_interest._sep)
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
            topicid = request.args.get('topicid')
            topiclabel = request.args.get('topiclabel')
            find_topic = Interests.query(Interests.topic == topiclabel)
            this_topics_list = find_topic.fetch()

            if len(this_topics_list) > 0:
                return "This topic is already present", 200
            else:
                this_interest = Interests()
                this_interest.write_topic_id(id=topicid)
                this_interest.write_topic(topic=topiclabel)
                this_interest.put()
                return "Topic successfully created", 200

        elif is_login_route(route=route_list):
            _route = request.args.get("route_list")
            return route_login_post(route=_route)
        elif "games" in route_list:
            _route = request.args.get('route_list')
            if route_list == "tetris":
                return route_tetris()
            elif route_list == "pacman":
                return route_pacman()
            elif route_list == "chess":
                return route_chess()
            elif route_list == "checkers":
                return route_checkers()
            elif route_list == "pingpong":
                return route_ping_pong()
            elif route_list == "matrix":
                return route_matrix()

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

        elif "blog" in route_list or "blog.html" in route_list:
            return route_blog()

        elif "strange" in route_list and "algorithms" in route_list:
            return route_strange()

        elif "perlin" in route_list and "algorithms" in route_list:
            return route_perlin()

        elif "matrix" in route_list and "algorithms" in route_list:
            return route_matrix()

        elif "gameoflife" in route_list and "algorithms" in route_list:
            return route_life()

        elif "maze" in route_list and "algorithms" in route_list:
            return route_maze()

        elif "path" in route_list and "algorithms" in route_list:
            return route_path()

        elif "matter" in route_list and "algorithms" in route_list:
            return route_matter()

        elif "plinko" in route_list and "algorithms" in route_list:
            return route_plinko()

        elif "mazesolver" in route_list and "algorithms" in route_list:
            return route_maze_solver()

        elif "algorithms" in route_list or "algorithms.html" in route_list:
            return route_algorithms()

        elif "dashboard" in route_list or "dashboard.html" in route_list:
            return route_dashboard()

        elif "games" in route_list or "games.html" in route_list:
            return route_games()
        elif "matrix" in route_list:
            return route_matrix()
        elif "snake" in route_list:
            return route_snake()

        elif "500" in route_list:
            return route_500()
        else:
            return route_home()
