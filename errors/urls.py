from django.conf.urls import url
from django.urls import path
from .views import issue_tracker, issue_detail, add_comment, delete_comment

urlpatterns = [
    url(r'^$', issue_tracker, name="issue_tracker"),
    url(r'^comment/add/(?P<issue_id>\d+)', add_comment, name="add_comment"),
    url(r'^comment/delete/(?P<comment_id>\d+)', delete_comment, name="delete_comment"),
    url(r'^(?P<issue_id>\d+)', issue_detail, name="issue_detail"),
]