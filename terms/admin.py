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
    list_display = ('__str__', 'name', 'url', 'case_sensitive')
    list_editable = ('name', 'url', 'case_sensitive')
    search_fields = ('name', 'definition', 'url')

    def get_changelist_form(self, request, **kwargs):
        kwargs['form'] = self.form
        return super(TermAdmin, self).get_changelist_form(request, **kwargs)


site.register(Term, TermAdmin)
