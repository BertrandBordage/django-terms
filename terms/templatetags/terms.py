# coding: utf-8

from django.template import Library
from django.template.defaultfilters import stringfilter
from ..html import replace_in_html

register = Library()


@register.filter
@stringfilter
def replace_terms(html):
    return unicode(replace_in_html(html))
