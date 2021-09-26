from django.urls import path, include
from .views import Login, logout, Register, change_password, users_builds, settings, update_profile, delete_account
from accounts import urls_reset

urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('register/', Register.as_view(), name="register"),
    path('logout/', logout, name="logout"),
    path('password-reset/', include(urls_reset)),
    path('change-password/', change_password, name="change_password"),
    path('update-profile/', update_profile, name="update_profile"),
    path('delete-account/', delete_account, name="delete_account"),
    path('settings/', settings, name="settings"),
    path('<str:username>', users_builds, name="users_builds"),
]