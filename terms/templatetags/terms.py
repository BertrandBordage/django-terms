# coding: utf-8

from django.template import Library
from django.template.defaultfilters import stringfilter
from ..html import replace_terms

register = Library()


register.filter(stringfilter(replace_terms))
