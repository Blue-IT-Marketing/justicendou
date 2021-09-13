
import os
import jinja2
import logging
import datetime
import requests
from google.cloud import ndb
from src.accounts import Accounts
from src.articles import Articles, this_topics

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))
#import firebase_admin
#from firebase_admin import credentials
#cred = credentials.Certificate('templates/firebase/service_account.json')
#default_app = firebase_admin.initialize_app(cred)
from flask import Blueprint, make_response, render_template

main_router_bp = Blueprint('main_router_handler', __name__)

def route_sitemap(self):
    #TODO- Consider creating a dynamic sitemap by actually crawling my site and then outputting the sitemap here
    #TODO- i think i use to have a function to do this coupled with thoth
    response = make_response(render_template('templates/sitemap/sitemap.xml'))
    response.headers["Content-Type"] = 'text/xml'
    return response, 200

def route_robots(self):
    response  = make_response(render_template('templates/sitemap/robots.txt'))
    response.headers["Content-Type"] = "text/plain"
    return response, 200

def route_home(self):
    import random
    this_articles = Articles()
    #this_articles.save_topics()

    topic = random.choice(this_topics)
    articles = this_articles.fetch_topic(topic=topic)

    if articles != "":
        articles = articles['articles']
    return render_template('templates/index.html', articles=articles), 200

def route_login(self):
    return render_template('templates/authentication/login.html'), 200

def route_logout(self):
    return render_template('templates/authentication/logout.html'), 200

def route_about(self):
    return render_template('templates/about.html'), 200

def route_contact(self):
    return render_template('templates/contact/contact.html')

def route_blog(self):
    return render_template("templates/blog/home.html")

def route_algorithms(self):
    return render_template("templates/algorithms/algos.html")

def route_strange(self):
    return render_template("templates/algorithms/strange/strange.html")

def route_perlin(self):
    return render_template("templates/algorithms/perlin/perlin.html")

def route_life(self):
    return render_template("templates/algorithms/gameoflife/life.html")

def route_maze(self):
    return render_template("templates/algorithms/maze/maze.html")


def route_path(self):
    return render_template("templates/algorithms/pathfinder/path.html")


def RouteMatter(self):
    template = template_env.get_template("templates/algorithms/matter/matter.html")
    context = {}
    self.response.write(template.render(context))



@main_router_bp.route('/', methods=['GET', 'POST', 'DELETE', 'PUT'])

def main_router_handler():
    pass




    def RouteDashboard(self):

        if users.is_current_user_admin():
            logout_url = users.create_logout_url(dest_url='/')
            # logout_url = ''
            template = template_env.get_template("templates/dashboard/dashboard.html")
            context = {'logout_url':logout_url}
            self.response.write(template.render(context))
        else:
            login_url = users.create_login_url(dest_url='/dashboard')
            template = template_env.get_template("templates/lockscreen.html")
            context = {'login_url':login_url}
            self.response.write(template.render(context))

    def RouteGames(self):
        template = template_env.get_template("templates/games/games.html")
        context = {}
        self.response.write(template.render(context))

    def RouteTetris(self):
        template = template_env.get_template("templates/games/tetris/tetris.html")
        context = {}
        self.response.write(template.render(context))

    def RoutePacman(self):
        template = template_env.get_template("templates/games/pacman/pacman.html")
        context = {}
        self.response.write(template.render(context))

    def RouteChess(self):
        template = template_env.get_template("templates/games/garbo/chess.html")
        context = {}
        self.response.write(template.render(context))

    def RouteCheckers(self):
        template = template_env.get_template("templates/games/checkers/checkers.html")
        context = {}
        self.response.write(template.render(context))


    def RoutePingPong(self):
        template = template_env.get_template("templates/games/pingpong/pingpong.html")
        context = {}
        self.response.write(template.render(context))

    def RouteMatrix(self):
        template = template_env.get_template("templates/games/matrix/matrix.html")
        context = {}
        self.response.write(template.render(context))

    def RouteSnake(self):
        template = template_env.get_template("templates/games/snake/snake.html")
        context = {}
        self.response.write(template.render(context))

    def RoutePlinko(self):
        template = template_env.get_template("templates/algorithms/plinko/plinko.html")
        context = {}
        self.response.write(template.render(context))

        
    def RouteMazeSolver(self):
        template = template_env.get_template("templates/algorithms/mazepath/mazepath.html")
        context = {}
        self.response.write(template.render(context))
        
        
        
    def RouteDashboardPost(self,route):
        from services import HireMe

        if route == "hireme":
            
            find_hires = HireMe.query(HireMe.project_status <> "completed")
            this_hires_list = find_hires.fetch()
            
            template = template_env.get_template('templates/dashboard/hireme.html')
            context = {'this_hires_list':this_hires_list}
            self.response.write(template.render(context))

        elif route == "get-project": # dashboard project get
            projectid = self.request.get('projectid')
            find_hires = HireMe.query(HireMe.projectid == projectid)
            this_hires_list = find_hires.fetch()
            if len(this_hires_list) > 0:
                this_hire = this_hires_list[0]
                template = template_env.get_template('templates/dashboard/project.html')
                context ={'this_hire':this_hire} 
                self.response.write(template.render(context))
            else:
                this_hire = HireMe()
                template = template_env.get_template('templates/dashboard/project.html')
                context ={'this_hire':this_hire} 
                self.response.write(template.render(context))
                
        elif route == "update-project": #dashboard project updater
            projectid = self.request.get('projectid')
            names = self.request.get('names')
            cell = self.request.get('cell')
            email = self.request.get('email')
            website = self.request.get('website')
            facebook = self.request.get('facebook')
            twitter = self.request.get('twitter')
            company = self.request.get('company')
            freelancing = self.request.get('freelancing')
            project_type = self.request.get('project-type')
            project_title = self.request.get('project-title')
            project_description = self.request.get('project-description')
            estimated_budget = self.request.get('estimated-budget')
            start_date = self.request.get('start-date')
            project_status = self.request.get('project-status')

            start_date = convert_datestring_to_datetime(start_date)



            find_project = HireMe.query(HireMe.projectid == projectid)
            this_project_list = find_project.fetch()
            if len(this_project_list) > 0:
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

            self.response.write("project succesfully updated")


        elif route == "messages":
            template = template_env.get_template('templates/dashboard/messages.html')
            context = {}
            self.response.write(template.render(context))

        elif route == "interests":
            find_topics = Interests.query()
            interests_list = find_topics.fetch()
            template = template_env.get_template('templates/dashboard/interests.html')
            context = {'interests_list':interests_list}
            self.response.write(template.render(context))


        elif route == "createpage":
            template = template_env.get_template('templates/dashboard/createpage.html')
            context = {}
            self.response.write(template.render(context))

        elif route == "createposts":
            template = template_env.get_template('templates/dashboard/createposts.html')
            context = {}
            self.response.write(template.render(context))

        elif route == "subjectfromtopicid":
            topicid = self.request.get('topicid')
            find_subjects = Interests.query(Interests.topic_id == topicid)
            this_interests_list = find_subjects.fetch()
            if len(this_interests_list) > 0:
                
                this_interest = this_interests_list[0] 
                #this_subjects_list = this_interest.subjects.split(this_interest._sep)
                #logging.info(this_subjects_list)
                self.response.write(this_interest.subjects)

        elif route == "addsubjectstotopicid":
            topicid = self.request.get('topicid')
            subjects_list = self.request.get('subjects-list')
            find_subjects = Interests.query(Interests.topic_id == topicid)
            this_interests_list = find_subjects.fetch()
            if len(this_interests_list) > 0:
                this_interest = this_interests_list[0]
            else:
                this_interest = Interests()

            this_interest.write_topic_id(id=topicid)            
            subjects_list = subjects_list.split(this_interest._sep)
            for subject in subjects_list:
                this_interest.write_subjects(subject=subject)
            
            this_interest.put()
            self.response.write("completed adding subjects")

        elif route == "removesubjectstopicid":
            topicid = self.request.get('topicid')
            subjects_list = self.request.get('subjects-list')
            find_subjects = Interests.query(Interests.topic_id == topicid)
            this_interests_list = find_subjects.fetch()
            if len(this_interests_list) > 0:
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

                self.response.write("subjects removed")

        elif route == "createtopic":
            topicid = self.request.get('topicid')
            topiclabel = self.request.get('topiclabel')

            find_topic = Interests.query(Interests.topic == topiclabel)
            this_topics_list = find_topic.fetch()

            if len(this_topics_list) > 0:
                self.response.write("This topic is already present")
            else:
                this_interest = Interests()
                this_interest.write_topic_id(id=topicid)
                this_interest.write_topic(topic=topiclabel)
                this_interest.put()
                self.response.write("Topic successfully created")
            

    def Route404(self):
        template = template_env.get_template('templates/404.html')
        context = {}
        self.response.write(template.render(context))

    def Route500(self):
        template = template_env.get_template('templates/500.html')
        context = {}
        self.response.write(template.render(context))




    def RouteLoginPost(self,route):
        from accounts import Accounts
        #from firebase_admin import auth

        if route == "email-not-verified":
            template = template_env.get_template('templates/authentication/loggedin.html')
            context = {}
            self.response.write(template.render(context))

        elif route == "email-verified":
            template = template_env.get_template('templates/authentication/loggedin.html')
            context = {}
            self.response.write(template.render(context))

        elif route == "user-not-loggedin":
            template = template_env.get_template('templates/authentication/loggedout.html')
            context = {}
            self.response.write(template.render(context))

        elif route == "2":
            vstrDisplayName = self.request.get('vstrDisplayName')
            vstrEmail = self.request.get('vstrEmail')
            vstremailVerified = self.request.get('vstremailVerified')
            vstrUserID = self.request.get('vstrUserID')
            vstrPhoneNumber = self.request.get('vstrPhoneNumber')
            vstrProviderData = self.request.get('vstrProviderData')
            vstrAccessToken = self.request.get('vstrAccessToken')

            #decode_token = auth.verify_id_token(vstrAccessToken)
            #uid = decode_token['uid']

            findRequest = Accounts.query(Accounts.strUserID == vstrUserID)
            thisAccountList = findRequest.fetch()

            if len(thisAccountList) > 0:
                thisAccount = thisAccountList[0]
                thisAccount.writeEmail(strinput=vstrEmail)

            else:
                findRequest = Accounts.query(Accounts.strEmail == vstrEmail)
                thisAccountList = findRequest.fetch()
                if len(thisAccountList) > 0:
                    thisAccount = thisAccountList[0]
                    thisAccount.writeUserID(strinput=vstrUserID)
                else:
                    thisAccount = Accounts()
                    thisAccount.writeUserID(strinput=vstrUserID)
                    thisAccount.writeNames(strinput=vstrDisplayName)
                    thisAccount.writeEmail(strinput=vstrEmail)
                    thisAccount.writeProviderData(strinput=vstrProviderData)


            if vstremailVerified == "YES":
                thisAccount.writeVerified(strinput=True)
            else:
                thisAccount.writeVerified(strinput=False)
                thisAccount.writeUserID(strinput=vstrUserID)
                thisAccount.writeCell(strinput=vstrPhoneNumber)
                thisAccount.writeProviderData(strinput=vstrProviderData)

            thisAccount.writeAccessToken(strinput=vstrAccessToken)
            thisAccount.put()

            #TODO - Refine this part


    def get(self):
        """
            The Main Get Router entry point
        :return:
        """
        URL = self.request.url
        URL = str(URL)
        URL = URL.lower()
        strURLlist = URL.split("/")

        logging.info(str(len(strURLlist)))

        if len(strURLlist) >= 4:

            if ("index" in strURLlist) or ("index.html" in strURLlist):
                self.route_home()
            elif ("login" in strURLlist) or ("login.html" in strURLlist) or ("signin" in strURLlist) or ("signin.html" in strURLlist) or ("subscribe" in strURLlist) or ("subscribe.html" in strURLlist):
                self.RouteLogin()

            elif ("logout" in strURLlist) or ("logout.html" in strURLlist) or ("signout" in strURLlist) or ("signout.html" in strURLlist):
                self.route_logout()

            elif "sitemap.xml" in strURLlist:
                self.route_sitemap()

            elif "robots.txt" in strURLlist:
                self.route_robots()

            elif ("about" in strURLlist) or ("about.html" in strURLlist):
                self.route_about()

            elif ("contact" in strURLlist) or ("contact.html" in strURLlist):
                self.route_contact()

            elif ("blog" in strURLlist) or ("blog.html" in strURLlist):
                self.route_blog()

            elif ("strange" in strURLlist) and ("algorithms" in strURLlist):
                self.RouteStrange()

            elif ("perlin" in strURLlist) and ("algorithms" in strURLlist):
                self.RoutePerlin()

            elif ("matrix" in strURLlist) and ("algorithms" in strURLlist):
                self.RouteMatrix()

            elif ("gameoflife" in strURLlist) and ("algorithms" in strURLlist):
                self.RouteLife()

            elif ("maze" in strURLlist) and ("algorithms" in strURLlist):
                self.route_maze()

            elif ("path" in strURLlist) and ("algorithms" in strURLlist):
                self.route_path()


            elif ("matter" in strURLlist) and ("algorithms" in strURLlist):
                self.RouteMatter()

            elif ("plinko" in strURLlist) and ("algorithms" in strURLlist):
                self.RoutePlinko()

            elif ("mazesolver" in strURLlist) and ("algorithms" in strURLlist):
                self.RouteMazeSolver()


            elif ("algorithms" in strURLlist) or ("algorithms.html" in strURLlist):
                self.route_algorithms()

            elif ("dashboard" in strURLlist) or("dashboard.html" in strURLlist):
                self.RouteDashboard()

            elif ("games" in strURLlist) or ("games.html" in strURLlist):
                self.RouteGames()
            elif ("matrix" in strURLlist):
                self.RouteMatrix()
            elif ("snake" in strURLlist):
                self.RouteSnake()

            elif ("500" in strURLlist):
                self.Route500()
            else:
                self.route_home()
        else:
            self.route_home()

    def post(self):
        """
            The Main Post Router will also have sub routers for login and logout
        :return:
        """
        URL = self.request.url
        URL = str(URL)
        URL = URL.lower()
        strURLlist = URL.split("/")
        if len(strURLlist) == 4:
            if ("login" in strURLlist) or ("login.html" in strURLlist) or ("signin" in strURLlist) or ("signin.html" in strURLlist) or ("subscribe" in strURLlist) or ("subscribe.html" in strURLlist):
                route = self.request.get("route")
                self.RouteLoginPost(route=route)
            elif ("games" in strURLlist):
                route = self.request.get('route')
                if route == "tetris":
                    self.RouteTetris()
                elif route == "pacman":
                    self.RoutePacman()
                elif route == "chess":
                    self.RouteChess()
                elif route == "checkers":
                    self.RouteCheckers()
                elif route == "pingpong":
                    self.RoutePingPong()
                elif route == "matrix":
                    self.RouteMatrix()


            elif ("dashboard" in strURLlist):
                route = self.request.get('route')
                self.RouteDashboardPost(route=route)
                
        else:
            pass


class DashboardHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/dashboard/dashboard.html')
        context = {}
        self.response.write(template.render(context))



app = webapp2.WSGIApplication([
    
    
    ('.*', MainRouterHandler)

], debug=True)
