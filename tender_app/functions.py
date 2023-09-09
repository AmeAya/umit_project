from django.core.mail import send_mail
from django.conf import settings


def sendEmail(email: str, code: str) -> None:
    subject = 'Your code to Umit Project'
    message = 'Your confirmation code:\n' + code
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)

