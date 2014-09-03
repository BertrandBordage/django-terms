# coding: utf-8

from __future__ import unicode_literals
import sys
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models import Model, CharField, TextField, BooleanField
from django.utils.translation import ugettext_lazy as _
from .managers import TermManager, CACHE_KEYS


def python_2_unicode_compatible(klass):
    # Taken from django.utils.encoding
    PY3 = sys.version_info[0] == 3
    if not PY3:
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return klass


@python_2_unicode_compatible
class Term(Model):
    name = CharField(
        _('name'), max_length=100, unique=True, help_text=_(
            'Variants of the name can be specified with a “|” separator '
            '(e.g. “name|names|to name”).'))
    case_sensitive = BooleanField(_('case sensitive'), default=False)
    definition = TextField(_('definition'), blank=True,
                           help_text=_('Accepts HTML tags.'))
    url = CharField(_('link'), max_length=200, blank=True,
                    help_text=_('Address to which the term will redirect '
                                '(instead of redirecting to the definition).'))

    objects = TermManager()

    class Meta(object):
        verbose_name = _('term')
        verbose_name_plural = _('terms')
        ordering = ('name',)

    def __str__(self):
        return self.original_name

    def save(self, *args, **kwargs):
        cache.delete_many(CACHE_KEYS)
        super(Term, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.url:
            return self.url
        return reverse('term', kwargs={'pk': self.pk})

    def name_variants(self, variant_slice=slice(0, None)):
        return self.name.replace('&', '&amp;').split('|')[variant_slice]

    @property
    def original_name(self):
        return self.name_variants(0)
