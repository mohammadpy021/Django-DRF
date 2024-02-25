from celery import shared_task

@shared_task
def email_send(mail_object):
    mail_object.send(fail_silently=False)
    