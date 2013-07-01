# coding: utf-8

import re
from django.core.cache import cache
from django.db.models import Manager
from django.template.loader import render_to_string


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
            for term in self.get_query_set():
                name_variants = term.name_variants()
                for variant in name_variants:
                    d[variant.lower()] = name_variants
            cache.set(VARIANTS_DICT_CACHE_KEY, d)
        return d

    def replace_dict(self):
        d = cache.get(REPLACE_DICT_CACHE_KEY)
        if d is None:
            d = {}
            template = 'terms/term_replace.html'
            for term in self.get_query_set():
                url = term.get_absolute_url()
                name_variants = term.name.split('|')
                context = {'url': url.replace('%', '%%'),
                           'url_is_external': bool(term.url)}
                case_sensitive = term.case_sensitive
                for name_variant in name_variants:
                    d[name_variant.lower()] = render_to_string(template, context), case_sensitive
            cache.set(REPLACE_DICT_CACHE_KEY, d)
        return d

    def replace_regexp(self):
        r = cache.get(REPLACE_REGEXP_CACHE_KEY)
        if r is None:
            terms = sorted(self.replace_dict().keys(), key=len, reverse=True)
            r = re.compile('(?P<before>^|\W)(?P<name>%s)(?P<after>\W|$)'
                           % '|'.join(map(re.escape, terms)),
                           flags=re.IGNORECASE)
            cache.set(REPLACE_REGEXP_CACHE_KEY, r)
        return r
