# coding: utf-8

from django.template import Library
from django.template.defaultfilters import stringfilter
try:
    from django.utils.encoding import smart_text
except ImportError:  # For Django < 1.4.2
    from django.utils.encoding import smart_unicode as smart_text
from ..html import replace_in_html

register = Library()


@register.filter
@stringfilter
def replace_terms(html):
    return smart_text(replace_in_html(html))
