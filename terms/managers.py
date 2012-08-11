# coding: utf-8

from django.db.models import Manager
from django.core.cache import cache
from django.template.loader import render_to_string
import re


REPLACE_DICT_CACHE_KEY = 'terms__replace_dict'
REPLACE_REGEXP_CACHE_KEY = 'terms__replace_regexp'
CACHE_KEYS = REPLACE_DICT_CACHE_KEY, REPLACE_REGEXP_CACHE_KEY


class TermManager(Manager):
    def replace_dict(self):
        d = cache.get(REPLACE_DICT_CACHE_KEY, {})
        if d:
            return d
        t = 'terms/term_replace.html'
        for term in self.get_query_set().iterator():
            d[term.name] = render_to_string(t, {'term': term})
        cache.set(REPLACE_DICT_CACHE_KEY, d)
        return d

    def replace_regexp(self):
        r = cache.get(REPLACE_REGEXP_CACHE_KEY, None)
        if r is not None:
            return r
        replace_dict = self.replace_dict()
        r = re.compile('(?P<before>^|\W)(?P<term>%s)(?P<after>\W|$)'
                       % '|'.join(map(re.escape, replace_dict)))
        cache.set(REPLACE_REGEXP_CACHE_KEY, r)
        return r
