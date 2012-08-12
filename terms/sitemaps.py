from django.contrib.sitemaps import Sitemap
from .models import Term


class TermsSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.1

    def items(self):
        return Term.objects.all()
