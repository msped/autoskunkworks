from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class SupportStaticSitemap(Sitemap):
    priority = 0.6

    def items(self):
        return ['support']

    def location(self, item):
        return reverse(item)