from django.core.mail import send_mail
from django.template import loader
from django.utils.html import strip_tags


def signup_email(request):
    """Send out email to confirm signup"""
    html_email = loader.render_to_string(
        'emails/signup.html',
    )
    message = strip_tags(html_email)
    send_mail(
        'Welcome to AutoSkunkWorks',
        message=message,
        from_email='autoskunkworks@gmail.com',
        fail_silently=False,
        connection=None,
        recipient_list=[str(request.user.email)],
        html_message=html_email
    )

def deactivate_email(request):
    """Send out email to confirm signup"""
    html_email = loader.render_to_string(
        'emails/deactivate_account.html',
    )
    message = strip_tags(html_email)
    send_mail(
        'Your AutoSkunkWorks Account has been deactivated.',
        message=message,
        from_email='autoskunkworks@gmail.com',
        fail_silently=False,
        connection=None,
        recipient_list=[str(request.user.email)],
        html_message=html_email
    )

