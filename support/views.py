import os
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.shortcuts import render
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from .forms import ContactForm

# Create your views here.


def support(request):
    """Support page view"""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message_form = form.cleaned_data['message']
            html_content = f'<p>New form submission</p> {message_form} \n \n From: {name} ({email})'
            send_mail(
                subject=f'Contact Form Submission - {subject}',
                html_message=html_content,
                message=strip_tags(html_content),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMINS,],
                fail_silently=False
            )
            template = render_to_string('message_sent.html')
        else:
            name = form['name'].value()
            email = form['email'].value()
            subject = form['subject'].value()
            message = form['message'].value()
            template = render_to_string(
                'form_with_errors.html',
                request=request,
                context={
                    'form': ContactForm(initial={
                        'name': name,
                        'email': email,
                        'subject': subject,
                        'message': message
                    }),
                    'form': form
                }
            )
        return HttpResponse(template)
    else:
        if request.user.is_authenticated:
            form = ContactForm(initial={'email': request.user.email})
        else:
            form = ContactForm()

    return render(request, "support.html", {'form': form})
