from django.conf.urls import url
from .views import support

urlpatterns = [
    url(r'^$', support, name="support"),
]