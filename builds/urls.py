from django.conf.urls import url
from .views import create_build, view_build, builds, like_build, dislike_build, users_builds

urlpatterns = [
    url(r'^create', create_build, name="create_build"),
    url(r'^(?P<build_id>\d+)', view_build, name="view_build"),
    url(r'^$', builds, name="builds"),
    url(r'^like/(?P<build_id>\d+)', like_build, name="like_build"),
    url(r'^dislike/(?P<build_id>\d+)', dislike_build, name="dislike_build"),
    url(r'^(?P<username>[\w.@+-]+)', users_builds, name="users_builds")
]