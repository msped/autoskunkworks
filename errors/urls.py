from django.conf.urls import url
from .views import issue_tracker

urlpatterns = [
    url(r'^$', issue_tracker, name="issue_tracker"),
]