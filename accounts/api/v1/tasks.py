from celery import shared_task
from django.core.mail import send_mail, EmailMessage


@shared_task
def email_send(subject, token, ToEmail):
    send_mail(subject, f"{token}", "from@gmail.com", [ToEmail], fail_silently=False)
