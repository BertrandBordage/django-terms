# coding: utf-8

from django.db.models import Model, CharField, TextField, URLField
from django.utils.translation import ugettext_lazy as _
from .managers import TermManager
from django.core.urlresolvers import reverse


class Term(Model):
    name = CharField(_('name'), max_length=100)
    definition = TextField(_('definition'), blank=True)
    url = URLField(_('link'), verify_exists=True, blank=True, null=True)
    objects = TermManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        if self.url:
            return self.url
        return reverse('term', kwargs={'pk': self.pk})
