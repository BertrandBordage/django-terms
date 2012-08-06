# coding: utf-8

from django.contrib.admin import site
from .models import Term
from .forms import TermForm
try:
    from reversion import VersionAdmin as ModelAdmin
except ImportError:
    from django.contrib.admin import ModelAdmin


class TermAdmin(ModelAdmin):
    model = Term
    form = TermForm


site.register(Term, TermAdmin)
