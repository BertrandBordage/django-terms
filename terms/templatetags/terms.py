# coding: utf-8

from django.template import Library
from ..html import TermsHTMLReconstructor
from ..models import Term

register = Library()


@register.filter
def replace_terms(html):
    parser = TermsHTMLReconstructor()
    parser.feed(html)
    return parser.out
