# coding: utf-8

from django.template import Library
from django.template.defaultfilters import stringfilter
from ..html import TermsHTMLReconstructor

register = Library()


@register.filter
@stringfilter
def replace_terms(html):
    parser = TermsHTMLReconstructor()
    parser.feed(html)
    return parser.out
