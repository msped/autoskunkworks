"""autoskunkworks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from home.views import home
from accounts.sitemaps import AccountsStaticSitemap
from home.sitemaps import HomeStaticSitemap
from builds.sitemaps import BuildsSitemap
from support.sitemaps import SupportStaticSitemap
from errors.sitemaps import IssuesSitemap, StaticIssueSitemap

sitemaps = {
    'accountStatic': AccountsStaticSitemap,
    'homeStatic': HomeStaticSitemap,
    'builds': BuildsSitemap,
    'supportStatic': SupportStaticSitemap,
    'issuesStatic': StaticIssueSitemap,
    'issues': IssuesSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('user/', include('accounts.urls')),
    path('builds/', include('builds.urls')),
    path('support/', include('support.urls')),
    path('issues/', include('errors.urls')),
    path('captcha/', include('captcha.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt",
                             content_type="text/plain"),
    ),
]

handler400 = 'errors.views.handler400'
handler403 = 'errors.views.handler403'
handler404 = 'errors.views.handler404'
handler500 = 'errors.views.handler500'
