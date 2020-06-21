from django.conf.urls import url
from .views import create_build, view_build

urlpatterns = [
    url(r'^create', create_build, name="create_build"),
    url(r'^(?P<build_id>\d+)', view_build, name="view_build"),
]