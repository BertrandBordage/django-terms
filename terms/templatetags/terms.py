# coding: utf-8

from django.template import Library
from django.template.defaultfilters import stringfilter
from ..html import replace_terms as replace_terms_util

register = Library()


@register.filter
@stringfilter
def replace_terms(html):
    return replace_terms_util(html)
