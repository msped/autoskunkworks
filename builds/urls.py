from django.conf.urls import url
from django.urls import path
from .views import (
    create_build,
    view_build,
    builds,
    like_build, 
    dislike_build,
    edit_build,
    delete_build,
    get_web_price,
    download_qrcode
)

urlpatterns = [
    url(r'^create', create_build, name="create_build"),
    url(r'^edit/(?P<build_id>\w+)', edit_build, name="edit_build"),
    url(r'^$', builds, name="builds"),
    url(r'^like/(?P<build_id>\d+)', like_build, name="like_build"),
    url(r'^dislike/(?P<build_id>\d+)', dislike_build, name="dislike_build"),
    url(r'^delete/(?P<build_id>\d+)', delete_build, name="delete_build"),
    url(r'^get-web-price', get_web_price, name="get_web_price"),
    path(r'qr-code/<str:build_id>', download_qrcode, name="download_qrcode"),
    url(r'^(?P<build_id>\w+)', view_build, name="view_build"),
]