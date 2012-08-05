# coding: utf-8

from django.contrib.admin import site
from .models import Term
try:
    from reversion import VersionAdmin as ModelAdmin
except ImportError:
    from django.contrib.admin import ModelAdmin


class TermAdmin(ModelAdmin):
    model = Term


site.register(Term, TermAdmin)
