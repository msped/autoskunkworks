import os
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader


def signup_email(request):
    """Send out email to confirm signup"""
    html_email = loader.render_to_string(
        'emails/signup.html',
    )
    send_mail(
        subject='You have signed up for AutoSkunkWorks',
        html_message=html_email,
        message=strip_tags(html_email),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email,],
        fail_silently=False
    )

def deactivate_email(request):
    """Send out email to confirm signup"""
    html_email = loader.render_to_string(
        'emails/deactivate_account.html',
    )    
    send_mail(
        subject='Your AutoSkunkWorks Account has been deactivated.',
        html_message=html_email,
        message=strip_tags(html_email),
        from_email= settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email,],
        fail_silently=False
    )

