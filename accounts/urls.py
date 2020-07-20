from django.conf.urls import url, include
from .views import login, logout, register, change_password, users_builds, settings, update_profile
from accounts import urls_reset

urlpatterns = [
    url(r'^login/', login, name="login"),
    url(r'^register/', register, name="register"),
    url(r'^logout/', logout, name="logout"),
    url(r'^password-reset/', include(urls_reset)),
    url(r'^change_password/', change_password, name="change_password"),
    url(r'^update_profile/', update_profile, name="update_profile"),
    url(r'^settings/', settings, name="settings"),
    url(r'^(?P<username>[\w.@+-]+)', users_builds, name="users_builds"),
]