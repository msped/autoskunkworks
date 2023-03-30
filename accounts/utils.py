import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.template import loader


def signup_email(request):
    """Send out email to confirm signup"""
    html_email = loader.render_to_string(
        'emails/signup.html',
    )
    message = Mail(
    from_email=settings.DEFAULT_FROM_EMAIL,
    to_emails=request.user.email,
    subject='You have signed up for AutoSkunkWorks',
    html_content=html_email)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)

def deactivate_email(request):
    """Send out email to confirm signup"""
    html_email = loader.render_to_string(
        'emails/deactivate_account.html',
    )
    message = Mail(
    from_email=settings.DEFAULT_FROM_EMAIL,
    to_emails=request.user.email,
    subject='Your AutoSkunkWorks Account has been deactivated.',
    html_content=html_email)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)

