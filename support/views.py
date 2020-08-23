from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from autoskunkworks.settings import EMAIL_HOST_USER
from .forms import ContactForm

# Create your views here.

def support(request):
    """Support page view"""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            message += f' \n from: {email}'
            send_mail(subject, message, email, [EMAIL_HOST_USER])

            data = {
                'sent': True
            }
        else:
            data = {
                'sent': False,
                'error': "Invalid Form"
            }
        return JsonResponse(data)
    else:
        if request.user.is_authenticated:
            form = ContactForm(initial={'email': request.user.email})
        else:
            form = ContactForm()

        content = {
            'form': form,
        }
    return render(request, "support.html", {'form': ContactForm})