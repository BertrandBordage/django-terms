from django.contrib.sitemaps import Sitemap
from django.db.models import Q
from .models import Term


class TermsSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.1

    def items(self):
        return Term.objects.filter(Q(url__startswith='/') | Q(url=''))
