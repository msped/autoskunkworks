from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class SupportStaticSitemap(Sitemap):

    def items(self):
        return ['support']

    def location(self, item):
        return reverse(item)