import os
import random
import string
from typing import List, Optional

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

    # noinspection PyUnusedLocal
    @staticmethod
    def send_response(self):
        sender_address = 'support@justice-ndou.site'
        # mail.send_mail(sender_address, self.email, self.subject, self.message)
        return True


class TicketUsers(ndb.Model):
    uid = ndb.StringProperty()
    names = ndb.StringProperty()
    surname = ndb.StringProperty()
    cell = ndb.StringProperty()
    email = ndb.StringProperty()
    website = ndb.StringProperty()

    def __bool__(self) -> bool:
        return bool(self.uid)


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
    date_created = ndb.DateProperty(auto_now_add=True)
    time_created = ndb.TimeProperty(auto_now_add=True)
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

    def write_thread_id(self, thread_id: str):
        self.thread_id = thread_id

    @staticmethod
    def create_thread_id():
        return "".join(random.choices(string.digits + string.ascii_lowercase, k=32))

    def __bool__(self) -> bool:
        return bool(self.ticket_id)


class Comments(ndb.Model):
    author_id = ndb.StringProperty()
    thread_id = ndb.StringProperty()
    comment_id = ndb.StringProperty()  # a Sixteen Character Long ID Identifying this comment
    comment = ndb.StringProperty()
    comment_date = ndb.DateProperty()
    comment_time = ndb.TimeProperty()
    client_comment = ndb.BooleanProperty(default=True)


@contact_handler_bp.route('/contact/tickets/<string:path>', methods=['POST', 'GET'])
def default_contact_handler(path: str):
    if request.method == "GET":
        return render_template('contact/contact.html'), 200

    elif request.method == "POST":
        choice = request.args.get('choice')
        if choice == "0":
            # '&uid=' + struid + '&access_token=' + accessToken;
            uid = request.args.get('uid')
            access_token = request.args.get('access_token')

            cell, email, message, names, subject = gather_contact_details()

            contact_message = ContactMessages(message_reference=uid, names=names, email=email, cell=cell,
                                              subject=subject, message=message)
            contact_message.put()
            return """Contact Message Submitted Successfully One of our Representatives will get back to you 
            as soon as possible""", 200

        elif choice == "1":
            uid: str = request.args.get('uid')
            return render_template('contact/sub/subcontact.html', ticket_user=get_ticket_user(uid)), 200

        elif choice == "2":
            # TODO- need to pre load tickets for the current user
            # '&uid=' + struid + '&email=' + email + '&access_token=' + accessToken;
            uid = request.args.get('uid')
            template = template_env.get_template('contact/sub/tickets.html')
            return template.render(dict(ticket_user=get_ticket_user(uid),
                                        tickets_list=Tickets.query(Tickets.uid == uid).fetch())), 200

        elif choice == "3":
            uid = request.args.get('uid')
            access_token = request.args.get('access_token')

            body, cell, department, email, names, subject, surname, ticket_preference = gather_message_details()

            ticket_user = TicketUsers.query(TicketUsers.uid == uid).get()
            if not isinstance(ticket_user, TicketUsers) or not bool(ticket_user):
                key = TicketUsers(uid=uid, names=names, surname=surname, cell=cell, email=email).put()

            key = Tickets(uid=uid, ticket_id=create_id(), subject=subject, body=body,
                          ticket_preference=ticket_preference, department=department).put()

            return "Ticket Successfully created", 200

            # TODO- finish this up once done resolving the account issues

        elif choice == "4":
            uid = request.args.get('uid')
            email = request.args.get('email')
            access_token = request.args.get('access_token')
            # TODO finish this
            return render_template('contact/sub/address.html'), 200


def gather_contact_details():
    """
        **gather_contact_details**
            obtains contact details from request. args
    :return:
    """
    names = request.args.get('names')
    email = request.args.get('email')
    cell = request.args.get('cell')
    subject = request.args.get('subject')
    message = request.args.get('message')
    return cell, email, message, names, subject


def gather_message_details():
    """
        **gather_message_details**
            obtains and returns message details from args
    :return:
    """
    subject = request.args.get("subject")
    body = request.args.get("body")
    ticket_preference = request.args.get("ticket_preference")
    department = request.args.get("department")
    names = request.args.get("names")
    surname = request.args.get("surname")
    cell = request.args.get("cell")
    email = request.args.get("email")
    return body, cell, department, email, names, subject, surname, ticket_preference


def get_ticket_user(uid) -> Optional[TicketUsers]:
    """
        **get_ticket_user**
            given uid return Ticket User
    :param uid:
    :return:
    """
    ticket_user = TicketUsers.query(TicketUsers.uid == uid).get()
    return ticket_user if isinstance(ticket_user, TicketUsers) and bool(ticket_user.uid) else None


@contact_handler_bp.route('/contact', methods=['POST', 'GET'])
def return_contact():
    return render_template('contact/contact.html'), 200


@contact_handler_bp.route('/contact/read/<string:reference>', methods=['GET'])
def contact_reader(reference: str):
    query = ContactMessages.query(ContactMessages.message_reference == reference)
    contact_messages = query.fetch()
    contact_message = contact_messages[0] if contact_messages else ContactMessages()

    template = template_env.get_template('contact/readContact.html')
    context = {'contact_message': contact_message}
    return template.render(context), 200


@contact_handler_bp.route('/contact/tickets/<string:ticket_id>', methods=['POST', 'GET'])
def tickets_handler(ticket_id: str):
    if request.method == "GET":

        uid = request.args.get('uid')
        access_token = request.args.get('access_token')
        email = request.args.get('email')

        ticket_list, ticket_user = return_ticket_list(ticket_id, uid)

        if ticket_list:
            ticket_instance = ticket_list[0]

            query = CommentThread.query(CommentThread.ticket_id == ticket_instance.ticket_id).order(
                +CommentThread.datetime_created)
            comment_threads_list = query.fetch()
            if comment_threads_list:
                comment_thread = comment_threads_list[0]

                comment_threads_list = comment_thread.read_comments()
                comments_list = []
                for comm_id in comment_threads_list:
                    query = Comments.query(Comments.comment_id == comm_id,
                                           Comments.thread_id == comment_thread.thread_id)
                    temp_list = query.fetch()
                    comments_list = temp_list
                comments_list.reverse()

            else:
                comment_thread = CommentThread()
                comment_thread.write_thread_id(thread_id=comment_thread.create_thread_id())
                comment_thread.write_ticket_id(ticket_id=ticket_instance.ticket_id)
                _now = datetime.datetime.now()
                this_date: datetime.date = datetime.date(year=_now.year, month=_now.month,
                                                         day=_now.day)

                this_time: datetime.time = datetime.time(hour=_now.hour, minute=_now.minute,
                                                         second=_now.second)

                _comment_id: str = create_id()
                _comment: str = "Welcome to our ticketing system a help desk staff member will attend to you soon"
                comment_instance = Comments(thread_id=comment_thread.thread_id, author_id=uid, comment_id=_comment_id,
                                            comment=_comment, comment_date=this_date, comment_time=this_time)
                comment_instance.put()

                comments_list = [comment_instance.to_dict()]
                comment_thread.add_comment_id(comment_id=comment_instance.comment_id)
                comment_thread.put()

            template = render_template('contact/sub/ticket_instance.html', ticket_user=ticket_user,
                                       ticket_instance=ticket_instance, comments_list=comments_list,
                                       comment_thread=comment_thread)
            return template, 200

    elif request.method == "POST":
        choice = request.args.get("choice")
        if choice == "0":
            # '&uid=' + uid + '$email=' + email + '&access_token=' + accessToken;

            email = request.args.get('email')
            access_token = request.args.get('access_token')

            comment = request.args.get("comment")
            ticket_id = request.args.get("ticket_id")
            thread_id = request.args.get("thread_id")
            uid = request.args.get("uid")

            comment_thread = CommentThread.query(CommentThread.thread_id == thread_id,
                                                      CommentThread.ticket_id == ticket_id).fetch()


            _now = datetime.datetime.now()
            this_date = _now.date()
            this_time = _now.time()

            if isinstance(comment_thread, CommentThread) and bool(comment_thread):
                _comment_id: str = create_id()

                comment_instance = Comments(thread_id=comment_thread.thread_id, author_id=uid,
                                            comment_id=create_id(), comment=comment, comment_date=this_date,
                                            comment_time=this_time)
                comment_thread.add_comment_id(comment_id=comment_instance.comment_id)
                comment_thread.put()
                comment_instance.put()

                query = Comments.query(Comments.thread_id == comment_thread.thread_id)
                comments_list = query.fetch()
                comments_list.reverse()

                return render_template('contact/sub/AutoUpdate.html', comments_list=comments_list), 200

        elif choice == "1":
            # '&uid=' + uid + '&email=' + email + '&access_token=' + accessToken
            email = request.args.get('email')
            access_token = request.args.get('access_token')
            uid = request.args.get("uid")

            ticket_id = request.args.get("ticket_id")
            ticket_list, ticket_user = return_ticket_list(ticket_id, uid)

            if ticket_list:
                ticket_instance = ticket_list[0]
                query = CommentThread.query(CommentThread.ticket_id == ticket_instance.ticket_id).order(
                    +CommentThread.datetime_created)
                comment_threads_list = query.fetch()
                if comment_threads_list:
                    comment_thread = comment_threads_list[0]

                    comment_id_list = comment_thread.read_comments()
                    comments_list = []
                    for comm_id in comment_id_list:
                        query = Comments.query(Comments.comment_id == comm_id,
                                               Comments.thread_id == comment_thread.thread_id)
                        comments_list = query.fetch()
                        if comments_list:
                            comments_list.append(comments_list[0])
                    comments_list.reverse()

                    template = render_template('contact/sub/AutoUpdate.html', ticket_user=ticket_user,
                                               ticket_instance=ticket_instance, comments_list=comments_list,
                                               comment_thread=comment_thread)
                    return template, 200


def return_ticket_list(ticket_id, uid):
    query = TicketUsers.query(TicketUsers.uid == uid)
    users_list = query.fetch()
    if users_list:
        ticket_user = users_list[0]
    else:
        ticket_user = TicketUsers()
    query = Tickets.query(Tickets.uid == uid, Tickets.ticket_id == ticket_id)
    ticket_list = query.fetch()
    return ticket_list, ticket_user


def create_id():
    return "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits,
                                  k=64))
