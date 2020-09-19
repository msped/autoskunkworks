from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Issue

class StaticIssueSitemap(Sitemap):
    priority = 0.3
    
    def items(self):
        return ['issue_tracker']

    def location(self, item):
        return reverse(item)

class IssuesSitemap(Sitemap):
    priority = 0.3

    def items(self):
        return Issue.objects.all()

    def location(self, item):
        return f'/issues/{item.id}'