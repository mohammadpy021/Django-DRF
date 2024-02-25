from django.core.mail import EmailMessage
import threading


class EmailThread(threading.Thread):
    def __init__(self, mail_object):
        # self.subject = subject
        # self.recipient_list = recipient_list
        # self.html_content = html_content
        self.mail_object = mail_object
        threading.Thread.__init__(self)

    def run (self):
        self.mail_object.send(fail_silently=False)


