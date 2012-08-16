# coding: utf-8

from django.db.models import Model, CharField, TextField, URLField
from django.utils.translation import ugettext_lazy as _
from .managers import TermManager, CACHE_KEYS
from HTMLParser import HTMLParser
from django.core.cache import cache
from django.core.urlresolvers import reverse


class Term(Model):
    name = CharField(_('name'), max_length=100, unique=True,
                     help_text=_(u'Variants of the name can be specified with '
                                 u'a “|” separator (e.g. “Name|name|names”).'))
    definition = TextField(_('definition'), blank=True,
                           help_text=_('Accepts HTML tags.'))
    url = URLField(_('link'), blank=True, null=True,
                   help_text=_('Address to which the term will redirect '
                               '(instead of redirecting to the definition).'))

    objects = TermManager()

    class Meta:
        verbose_name = _('term')
        verbose_name_plural = _('terms')
        ordering = ('name',)

    def __unicode__(self):
        return self.original_name

    def save(self, *args, **kwargs):
        HTMLParser.unescape.__func__(HTMLParser, self.name)
        cache.delete_many(CACHE_KEYS)
        super(Term, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.url:
            return self.url
        return reverse('term', kwargs={'pk': self.pk})

    def name_variants(self, variant_slice=slice(0, None)):
        return self.name.split('|')[variant_slice]

    @property
    def original_name(self):
        return self.name_variants(0)
