from celery import shared_task
from django.core.mail import send_mail, EmailMessage


@shared_task
def send_email_task(subject, token, to_email, from_email="from@gmail.com"):
    send_mail(subject, f"{token}", from_email, [to_email], fail_silently=False)
   


