from django.conf.urls import url
from .views import create_build

urlpatterns = [
    url(r'^create', create_build, name="create_build"),
]