# coding: utf-8

from django.db.models import Manager
from django.core.cache import cache
from django.template.loader import render_to_string
import re


VARIANTS_DICT_CACHE_KEY = 'terms__variants_dict'
REPLACE_DICT_CACHE_KEY = 'terms__replace_dict'
REPLACE_REGEXP_CACHE_KEY = 'terms__replace_regexp'
CACHE_KEYS = (VARIANTS_DICT_CACHE_KEY, REPLACE_DICT_CACHE_KEY,
              REPLACE_REGEXP_CACHE_KEY)


class TermManager(Manager):
    def variants_dict(self):
        d = cache.get(VARIANTS_DICT_CACHE_KEY)
        if d is None:
            d = {}
            for term in self.get_query_set().iterator():
                name_variants = term.name_variants()
                for variant in name_variants:
                    d[variant] = name_variants
            cache.set(VARIANTS_DICT_CACHE_KEY, d)
        return d

    def replace_dict(self):
        d = cache.get(REPLACE_DICT_CACHE_KEY)
        if d is None:
            d = {}
            template = 'terms/term_replace.html'
            for term in self.get_query_set().iterator():
                url = term.get_absolute_url()
                name_variants = term.name.split('|')
                context = {'url': url,
                           'url_is_external': bool(term.url)}
                for name_variant in name_variants:
                    context['name_variant'] = name_variant
                    d[name_variant] = render_to_string(template, context)
            cache.set(REPLACE_DICT_CACHE_KEY, d)
        return d

    def replace_regexp(self):
        r = cache.get(REPLACE_REGEXP_CACHE_KEY)
        if r is None:
            replace_dict = self.replace_dict()
            r = re.compile('(?P<before>^|\W)(?P<name>%s)(?P<after>\W|$)'
                           % '|'.join(map(re.escape, replace_dict)))
            cache.set(REPLACE_REGEXP_CACHE_KEY, r)
        return r
