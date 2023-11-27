from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class AccountsStaticSitemap(Sitemap):
    priorty = 0.7
    changefreq = 'yearly'

    def items(self):
        return ['login', 'register']

    def location(self, item):
        return reverse(item)