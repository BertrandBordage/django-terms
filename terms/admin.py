# coding: utf-8

from django.contrib.admin import site
from .models import Term
from .forms import TermForm
from django.conf import settings
from django.contrib.admin import ModelAdmin
if 'reversion' in settings.INSTALLED_APPS:
    from reversion import VersionAdmin as ModelAdmin


class TermAdmin(ModelAdmin):
    model = Term
    form = TermForm
    list_display = ('name', 'url')
    search_fields = ('name', 'definition', 'url')


site.register(Term, TermAdmin)
