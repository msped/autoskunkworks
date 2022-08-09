from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Builds

class BuildsSitemap(Sitemap):
    priorty = 0.8

    def items(self):
        return Builds.objects.all()

    def location(self, item):
        return reverse('view_build', build_id=item.id)