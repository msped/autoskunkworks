from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from sentry_sdk import last_event_id
from .models import Issue
from .forms import NewTicket

# Create your views here.

def handler404(request, exception):
    return render(request, "404.html", status=404)

def handler500(request, *args, **argv):
    return render(request, "500.html", {
        'sentry_event_id': last_event_id(),
    }, status=500)

def issue_tracker(request):
    """Show issue tracker"""
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = NewTicket(request.POST)
        if form.is_valid():
            issue_location = form.cleaned_data['issue_location'] 
            description = form.cleaned_data['description']
            Issue.objects.create(
                user=user,
                issue_location=issue_location,
                description=description
            )
            messages.success(request, "Ticket has been Opened, you can check it's progress under 'My Tickets'")
            return redirect('issue_tracker')
        else:
            messages.error(request, 'Invalid Form - please check that is has been filled out correctly.')
            return redirect('issue_tracker')
    open_issues = Issue.objects.filter(issue_open=True).order_by('-id')
    closed_issues = Issue.objects.filter(issue_open=False).order_by('-id')
    my_issues = Issue.objects.filter(user=user).order_by('-id')
    context = {
        'open_issues': open_issues,
        'closed_issues': closed_issues,
        'my_issues': my_issues,
        'newTicketForm': NewTicket
    }
    return render(request, "issue_tracker.html", context)
