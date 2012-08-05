# coding: utf-8

from django.db.models import Manager
from django.template.loader import render_to_string
import re


class TermManager(Manager):
    def replace_dict(self):
        t = 'terms/term_replace.html'
        d = {}
        for term in self.get_query_set().iterator():
            d[term.name] = render_to_string(t, {'term': term})
        return d

    def replace_regexp(self):
        replace_dict = self.replace_dict()
        return re.compile('|'.join(map(re.escape, replace_dict)))
