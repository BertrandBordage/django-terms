# coding: utf-8

import re
import django
from django.core.cache import cache
from django.db.models import Manager
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


VARIANTS_DICT_CACHE_KEY = 'terms__variants_dict'
REPLACE_DICT_CACHE_KEY = 'terms__replace_dict'
REPLACE_REGEXP_CACHE_KEY = 'terms__replace_regexp'
CACHE_KEYS = (VARIANTS_DICT_CACHE_KEY, REPLACE_DICT_CACHE_KEY,
              REPLACE_REGEXP_CACHE_KEY)


class TermManager(Manager):
    def _get_variants_dict(self, qs):
        variants_dict = {}
        for term in qs:
            name_variants = term.name_variants()
            for variant in name_variants:
                variants_dict[variant.lower()] = name_variants
        return variants_dict

    def _get_replace_dict(self, qs):
        replace_dict = {}
        template = 'terms/term_replace.html'
        for term in qs:
            url = term.get_absolute_url()
            name_variants = term.name_variants()
            context = {'url': url.replace('%', '%%'),
                       'url_is_external': bool(term.url),
                       'tooltip_span': _('Open in new window'),
                       'definition': term.definition}

            case_sensitive = term.case_sensitive
            for name_variant in name_variants:
                replace_dict[name_variant.lower()] = \
                    render_to_string(template, context), case_sensitive
        return replace_dict

    def _caches_dicts(self):
        """
        Caches variants_dict and replace_dict in a single database hit.
        """

        qs = (self.get_query_set() if django.VERSION < (1, 6)
              else self.get_queryset())

        variants_dict = self._get_variants_dict(qs)
        cache.set(VARIANTS_DICT_CACHE_KEY, variants_dict)

        replace_dict = self._get_replace_dict(qs)
        cache.set(REPLACE_DICT_CACHE_KEY, replace_dict)

        return variants_dict, replace_dict

    def variants_dict(self):
        variants_dict = cache.get(VARIANTS_DICT_CACHE_KEY)
        if variants_dict is None:
            return self._caches_dicts()[0]
        return variants_dict

    def replace_dict(self):
        replace_dict = cache.get(REPLACE_DICT_CACHE_KEY)
        if replace_dict is None:
            return self._caches_dicts()[1]
        return replace_dict

    def replace_regexp(self):
        r = cache.get(REPLACE_REGEXP_CACHE_KEY)
        if r is None:
            terms = sorted(self.replace_dict().keys(), key=len, reverse=True)
            r = re.compile('(?P<before>\A|\W)(?P<name>%s)(?=\W|\Z)'
                           % '|'.join(map(re.escape, terms)),
                           flags=re.IGNORECASE | re.UNICODE)
            cache.set(REPLACE_REGEXP_CACHE_KEY, r)
        return r
