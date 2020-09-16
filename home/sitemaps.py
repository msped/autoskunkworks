from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class HomeStaticSitemap(Sitemap):

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)