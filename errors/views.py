from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.contrib import messages
from sentry_sdk import last_event_id
from .models import Issue, Comments
from .forms import NewTicket, NewComment

# Create your views here.

def handler404(request, exception):
    return render(request, "404.html", status=404)

def handler500(request, *args, **argv):
    return render(request, "500.html", {
        'sentry_event_id': last_event_id(),
    }, status=500)

def issue_tracker(request):
    """Show issue tracker"""
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        my_issues = Issue.objects.filter(user=user).order_by('-id')
    else: 
        my_issues = None
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
    context = {
        'open_issues': open_issues,
        'closed_issues': closed_issues,
        'my_issues': my_issues,
        'newTicketForm': NewTicket
    }
    return render(request, "issue_tracker.html", context)

def issue_detail(request, issue_id):
    i = Issue.objects.get(id=issue_id)
    c = Comments.objects.filter(issue=i)
    return render(request, "issue_detail.html", {
        'issue': i,
        'comments': c,
        'new_comment': NewComment()
    })

def add_comment(request, issue_id):
    """Add a comment to database for issue"""
    if request.method == "POST":
        form = NewComment(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            issue = Issue.objects.get(id=issue_id)
            user = User.objects.get(id=request.user.id)
            Comments.objects.create(
                user=user,
                issue=issue,
                comment=comment
            )
            messages.success(request, 'Comment has been added.')
            return redirect('issue_detail', issue_id)
    return redirect('issue_detail', issue_id)

def delete_comment(request, comment_id):
    c = Comments.objects.get(id=comment_id)
    i = c.issue.id
    if request.user.id == c.user.id:
        c.delete()
        messages.success(request, 'Comment has been deleted.')
        return redirect('issue_detail', i)
        