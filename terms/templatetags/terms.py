# coding: utf-8

from django.template import Library
from ..html import TermsHTMLReconstructor

register = Library()


@register.filter
def replace_terms(html):
    parser = TermsHTMLReconstructor()
    parser.feed(html)
    return parser.out
