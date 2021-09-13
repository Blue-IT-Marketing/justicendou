import os
import random
import string
from typing import List

import jinja2
import datetime
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadValueError
from flask import Blueprint, request, render_template

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

contact_handler_bp = Blueprint('contact_handler', __name__)

ticket_handler_bp = Blueprint('ticket_handler_bp', __name__)


class ContactMessages(ndb.Model):
    message_reference = ndb.StringProperty()
    names = ndb.StringProperty()
    email = ndb.StringProperty()
    cell = ndb.StringProperty()
    subject = ndb.StringProperty()
    message = ndb.StringProperty()
    message_excerpt = ndb.StringProperty()

    date_submitted = ndb.DateProperty(auto_now_add=True)
    time_submitted = ndb.TimeProperty(auto_now_add=True)

    response_sent = ndb.BooleanProperty(default=False)

    def read_date_submitted(self) -> datetime.date:
        return self.date_submitted

    def read_time_submitted(self) -> datetime.time:
        return self.time_submitted

    def read_response_sent(self) -> bool:
        return self.response_sent

    def write_response_sent(self, response_sent: bool):
        try:
            self.response_sent = response_sent
        except BadValueError:
            raise BadValueError

    def read_names(self) -> str:
        return self.names

    def write_names(self, names: str):
        self.names = names

    def read_email(self) -> str:
        return self.email

    def write_email(self, email: str):
        self.email = email

    def read_cell(self) -> str:
        return self.cell

    def write_cell(self, cell: str):
        self.cell = cell

    def read_subject(self):
        return self.subject

    def write_subject(self, subject: str):
        self.subject = subject

    def read_message(self):
        return self.message

    def write_message(self, message: str):
        self.message = message
        mess_len = len(self.message)
        self.message_excerpt = self.message[0:16] if mess_len > 16 else self.message

    def send_response(self):
        try:
            sender_address = ('support@justice-ndou.site')
            # mail.send_mail(sender_address, self.email, self.subject, self.message)
            return True
        except:
            return False


class TicketUsers(ndb.Model):
    uid = ndb.StringProperty()
    names = ndb.StringProperty()
    surname = ndb.StringProperty()
    cell = ndb.StringProperty()
    email = ndb.StringProperty()
    website = ndb.StringProperty()


class StaffMembers(ndb.Model):
    uid = ndb.StringProperty()
    present_ticket_id = ndb.StringProperty()
    name = ndb.StringProperty()
    surname = ndb.StringProperty()
    department = ndb.StringProperty()
    skill_level = ndb.StringProperty(default="Beginner")  # Intermediate, Expert
    user_assigned = ndb.BooleanProperty(default=False)
    user_online = ndb.BooleanProperty(default=False)
    not_available = ndb.BooleanProperty(default=False)


class Tickets(ndb.Model):
    ticket_id = ndb.StringProperty()
    uid = ndb.StringProperty()
    subject = ndb.StringProperty()
    body = ndb.StringProperty()
    date_created = ndb.DateProperty()
    time_created = ndb.TimeProperty()
    ticket_open = ndb.BooleanProperty(default=True)  # Ticket Open or Close
    ticket_preference = ndb.StringProperty(default="Normal")  # Normal / Urgent
    department = ndb.StringProperty(default="Sales")  # Programming, Hosting

    ticket_escalated = ndb.BooleanProperty(default=False)
    assigned_to = ndb.StringProperty()  # Assigned to Carries the ID of the Staff Member assigned the ticket
    escalated_to_uid = ndb.StringProperty()  # Staff Member the Ticket is Escalated To


class CommentThread(ndb.Model):
    ticket_id = ndb.StringProperty()
    thread_id = ndb.StringProperty()
    comments_list = ndb.StringProperty()  # a Comma Separated String with IDS of the comments in order
    datetime_created = ndb.DateTimeProperty(auto_now_add=True)

    def add_comment_id(self, comment_id: str):
        if len(comment_id) == 16:
            if self.comments_list is None:
                self.comments_list = comment_id
            else:
                self.comments_list += "," + comment_id

    def read_comments(self) -> List[str]:
        return self.comments_list.split(",") if self.comments_list else []

    def remove_comment_id(self, comment_id):
        if not self.comments_list:
            return

        comment_list = self.read_comments()
        if comment_id in comment_list:
            comment_list.remove(comment_id)
            self.comments_list = ",".join(comment_list)

    def write_ticket_id(self, ticket_id: str):
        self.ticket_id = ticket_id

    def write_thread_id(self, strinput):
        self.thread_id = strinput

    @staticmethod
    def create_thread_id():
        return "".join(random.choices(string.digits + string.ascii_lowercase, k=32))


class Comments(ndb.Model):
    author_id = ndb.StringProperty()
    thread_id = ndb.StringProperty()
    comment_id = ndb.StringProperty()  # a Sixteen Character Long ID Identifying this comment
    comment = ndb.StringProperty()
    comment_date = ndb.DateProperty()
    comment_time = ndb.TimeProperty()
    client_comment = ndb.BooleanProperty(default=True)


class ThisContactHandler():
    def get(self):
        # TODO - its easier to get session id if it exists
        # TODO- with the session then obtain userid
        # TODO- with the user id retrive the user account from the datastore and use that to retrieve user records

        template = template_env.get_template('templates/contact/contact.html')
        context = {}
        self.response.write(template.render(context))

    def post(self):


class ThisTicketHandler():
    def get(self):

        vstrUserID = request.args.get('vstrUserID')
        vstrAccessToken = request.args.get('vstrAccessToken')
        vstrEmail = request.args.get('vstrEmail')

        URL = self.request.url
        strURLlist = URL.split("/")
        strTicketID = strURLlist[len(strURLlist) - 1]

        findRequest = TicketUsers.query(TicketUsers.uid == vstrUserID)
        thisTicketUserList = findRequest.fetch()

        if len(thisTicketUserList) > 0:
            thisTicketUser = thisTicketUserList[0]
        else:
            thisTicketUser = TicketUsers()

        findRequest = Tickets.query(Tickets.uid == vstrUserID, Tickets.ticket_id == strTicketID)
        thisTicketList = findRequest.fetch()

        if len(thisTicketList) > 0:
            thisTicket = thisTicketList[0]

            findRequest = CommentThread.query(CommentThread.ticket_id == thisTicket.ticket_id).order(
                +CommentThread.datetime_created)
            thisCommentThreadsList = findRequest.fetch()
            if len(thisCommentThreadsList) > 0:
                thisThread = thisCommentThreadsList[0]

                strComIDList = thisThread.retrieveCommentsList()
                thisCommentList = []
                for thisComID in strComIDList:
                    findRequest = Comments.query(Comments.comment_id == thisComID,
                                                 Comments.thread_id == thisThread.thread_id)
                    commList = findRequest.fetch()
                    if len(commList) > 0:
                        thisCommentList.append(commList[0])
                thisCommentList.reverse()

            else:
                thisThread = CommentThread()
                thisThread.write_thread_id(strinput=thisThread.create_thread_id())
                thisThread.write_ticket_id(ticket_id=thisTicket.ticket_id)
                vstrThisDateTime = datetime.datetime.now()
                strThisDate = datetime.date(year=vstrThisDateTime.year, month=vstrThisDateTime.month,
                                            day=vstrThisDateTime.day)
                strThisTime = datetime.time(hour=vstrThisDateTime.hour, minute=vstrThisDateTime.minute,
                                            second=vstrThisDateTime.second)
                thisComment = Comments()
                thisComment.writeThreadID(strinput=thisThread.thread_id)
                thisComment.writeCommentID(strinput=thisComment.CreateCommentID())
                thisComment.writeAuthorID(strinput="000000")
                thisComment.writeIsClientComment(strinput=False)
                thisComment.writeCommentDate(strinput=strThisDate)
                thisComment.writeCommentTime(strinput=strThisTime)
                thisComment.writeComment(
                    strinput="Welcome to our ticketing system a help desk staff member will attend to you soon")
                thisComment.put()
                thisCommentList = []
                thisCommentList.append(thisComment)
                thisThread.add_comment_id(comment_id=thisComment.comment_id)
                thisThread.put()

            template = template_env.get_template('templates/contact/sub/thisTicket.html')
            context = {'thisTicketUser': thisTicketUser, 'thisTicket': thisTicket, 'thisCommentList': thisCommentList,
                       'thisThread': thisThread}
            self.response.write(template.render(context))

    def post(self):

        vstrChoice = request.args.get("vstrChoice")
        if vstrChoice == "0":
            # '&vstrUserID=' + vstrUserID + '$vstrEmail=' + email + '&vstrAccessToken=' + accessToken;

            vstrEmail = request.args.get('vstrEmail')
            vstrAccessToken = request.args.get('vstrAccessToken')

            vstrComment = request.args.get("vstrComment")
            vstrTicketID = request.args.get("vstrTicketID")
            vstrThreadID = request.args.get("vstrThreadID")
            vstrUserID = request.args.get("vstrUserID")

            findRequest = CommentThread.query(CommentThread.thread_id == vstrThreadID,
                                              CommentThread.ticket_id == vstrTicketID)
            thisCommentThreadList = findRequest.fetch()

            vstrThisDateTime = datetime.datetime.now()
            strThisDate = datetime.date(year=vstrThisDateTime.year, month=vstrThisDateTime.month,
                                        day=vstrThisDateTime.day)
            strThisTime = datetime.time(hour=vstrThisDateTime.hour, minute=vstrThisDateTime.minute,
                                        second=vstrThisDateTime.second)

            if len(thisCommentThreadList) > 0:
                thisCommentThread = thisCommentThreadList[0]
                thisComment = Comments()
                thisComment.writeThreadID(strinput=thisCommentThread.thread_id)
                thisComment.writeAuthorID(strinput=vstrUserID)
                thisComment.writeIsClientComment(strinput=True)
                thisComment.writeComment(strinput=vstrComment)
                thisComment.writeCommentID(strinput=thisComment.CreateCommentID())
                thisComment.writeCommentDate(strinput=strThisDate)
                thisComment.writeCommentTime(strinput=strThisTime)
                thisCommentThread.add_comment_id(comment_id=thisComment.comment_id)
                thisCommentThread.put()
                thisComment.put()

                findRequest = Comments.query(Comments.thread_id == thisCommentThread.thread_id)
                thisCommentList = findRequest.fetch()
                thisCommentList.reverse()
                template = template_env.get_template('templates/contact/sub/AutoUpdate.html')
                context = {'thisCommentList': thisCommentList}
                self.response.write(template.render(context))

        elif vstrChoice == "1":
            # '&vstrUserID=' + vstrUserID + '&vstrEmail=' + email + '&vstrAccessToken=' + accessToken
            vstrEmail = request.args.get('vstrEmail')
            vstrAccessToken = request.args.get('vstrAccessToken')
            vstrUserID = request.args.get("vstrUserID")

            vstrTicketID = request.args.get("vstrTicketID")
            findRequest = TicketUsers.query(TicketUsers.uid == vstrUserID)
            thisTicketUserList = findRequest.fetch()

            if len(thisTicketUserList) > 0:
                thisTicketUser = thisTicketUserList[0]
            else:
                thisTicketUser = TicketUsers()

            findRequest = Tickets.query(Tickets.uid == vstrUserID, Tickets.ticket_id == vstrTicketID)
            thisTicketList = findRequest.fetch()

            if len(thisTicketList) > 0:
                thisTicket = thisTicketList[0]

                findRequest = CommentThread.query(CommentThread.ticket_id == thisTicket.ticket_id).order(
                    +CommentThread.datetime_created)
                thisCommentThreadsList = findRequest.fetch()
                if len(thisCommentThreadsList) > 0:
                    thisThread = thisCommentThreadsList[0]

                    strComIDList = thisThread.retrieveCommentsList()
                    thisCommentList = []
                    for thisComID in strComIDList:
                        findRequest = Comments.query(Comments.comment_id == thisComID,
                                                     Comments.thread_id == thisThread.thread_id)
                        commList = findRequest.fetch()
                        if len(commList) > 0:
                            thisCommentList.append(commList[0])
                    thisCommentList.reverse()

                    template = template_env.get_template('templates/contact/sub/AutoUpdate.html')
                    context = {'thisTicketUser': thisTicketUser, 'thisTicket': thisTicket,
                               'thisCommentList': thisCommentList, 'thisThread': thisThread}
                    self.response.write(template.render(context))


class readContactHandler():
    def get(self):

        URL = self.request.url
        URLlist = URL.split("/")
        strReference = URLlist[len(URLlist) - 1]

        findRequest = ContactMessages.query(ContactMessages.message_reference == strReference)
        thisContactMessagesList = findRequest.fetch()

        if len(thisContactMessagesList) > 0:
            thisContactMessage = thisContactMessagesList[0]
        else:
            thisContactMessage = ContactMessages()

        template = template_env.get_template('templates/contact/readContact.html')
        context = {'thisContactMessage': thisContactMessage}
        self.response.write(template.render(context))


@contact_handler_bp.route('/contact/tickets/<string:path>', methods=['POST', 'GET'])
def default_contact_handler(path: str):
    if request.method == "GET":
        return render_template('templates/contact/contact.html'), 200

    elif request.method == "POST":

        choice = request.args.get('choice')

        if choice == "0":
            # '&uid=' + struid + '&access_token=' + accessToken;
            uid = request.args.get('uid')
            access_token = request.args.get('access_token')

            names = request.args.get('names')
            email = request.args.get('email')
            cell = request.args.get('cell')
            subject = request.args.get('subject')
            message = request.args.get('message')

            contact_message = ContactMessages()
            contact_message.message_reference = uid
            contact_message.write_names(names=names)
            contact_message.write_email(email=email)
            contact_message.write_cell(cell=cell)
            contact_message.write_subject(subject=subject)
            contact_message.writeMessage(strinput=message)

            contact_message.put()
            return """ Contact Message Submitted Successfully One of our Representatives will get back to you 
            as soon as possible """, 200

        elif choice == "1":
            # '&uid=' + struid + '&email=' + email + '&access_token=' + accessToken;
            uid = request.args.get('uid')
            email = request.args.get('email')
            access_token = request.args.get('access_token')

            query = TicketUsers.query(TicketUsers.uid == uid)
            ticket_user_list = query.fetch()
            if ticket_user_list:
                ticket_user = ticket_user_list[0]
            else:
                ticket_user = TicketUsers()

            template = template_env.get_template('templates/contact/sub/subcontact.html')
            context = {'ticket_user': ticket_user}
            return template.render(context), 200

        elif choice == "2":
            # TODO- need to pre load tickets for the current user
            # '&uid=' + struid + '&email=' + email + '&access_token=' + accessToken;
            uid = request.args.get('uid')
            email = request.args.get('email')
            access_token = request.args.get('access_token')

            query = TicketUsers.query(TicketUsers.uid == uid)
            ticket_user_list = query.fetch()
            if ticket_user_list:
                ticket_user = ticket_user_list[0]
            else:
                ticket_user = TicketUsers()

            query = Tickets.query(Tickets.uid == uid)
            tickets_list = query.fetch()

            template = template_env.get_template('templates/contact/sub/tickets.html')
            context = {'ticket_user': ticket_user, 'tickets_list': tickets_list}
            return template.render(context), 200

        elif choice == "3":
            # '&email=' + email + '&uid=' + struid + '&access_token=' + accessToken;
            uid = request.args.get('uid')
            access_token = request.args.get('access_token')

            subject = request.args.get("subject")
            body = request.args.get("body")
            ticket_preference = request.args.get("ticket_preference")
            department = request.args.get("department")
            names = request.args.get("names")
            surname = request.args.get("surname")
            cell = request.args.get("cell")
            email = request.args.get("email")

            query = TicketUsers.query(TicketUsers.uid == uid)
            ticket_user_list = query.fetch()

            if len(ticket_user_list) > 0:
                ticket_user = ticket_user_list[0]
            else:
                ticket_user = TicketUsers()
                ticket_user.writeUserID(strinput=uid)
                ticket_user.writeNames(strinput=names)
                ticket_user.writeSurname(strinput=surname)
                ticket_user.writeCell(strinput=cell)
                ticket_user.writeEmail(strinput=email)
                ticket_user.put()

            vstrThisDateTime = datetime.datetime.now()
            strThisDate = datetime.date(year=vstrThisDateTime.year, month=vstrThisDateTime.month,
                                        day=vstrThisDateTime.day)
            strThisTime = datetime.time(hour=vstrThisDateTime.hour, minute=vstrThisDateTime.minute,
                                        second=vstrThisDateTime.second)

            thisTicket = Tickets()
            thisTicket.writeUserID(strinput=uid)
            thisTicket.writeTicketID(strinput=thisTicket.CreateTicketID())
            thisTicket.writeSubject(strinput=subject)
            thisTicket.writeBody(strinput=body)
            thisTicket.writeTicketPreferences(strinput=ticket_preference)
            thisTicket.writeDepartment(strinput=department)
            thisTicket.writeDateCreated(strinput=strThisDate)
            thisTicket.writeTimeCreated(strinput=strThisTime)
            thisTicket.put()
            self.response.write("Ticket Successfully created")

            # TODO- finish this up once done resolving the account issues

        elif choice == "4":
            # '&uid=' + struid + '&email=' + email + '&access_token=' + accessToken;
            uid = request.args.get('uid')
            email = request.args.get('email')
            access_token = request.args.get('access_token')

            template = template_env.get_template('templates/contact/sub/address.html')
            context = {}
            self.response.write(template.render(context))


app = webapp2.WSGIApplication([

    ('/contact/tickets/.*', ThisTicketHandler),
    ('/contact/read/.*', readContactHandler),
    ('/contact', ThisContactHandler)

], debug=True)
