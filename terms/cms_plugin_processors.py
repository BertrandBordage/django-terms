# coding: utf-8

from django.utils.safestring import mark_safe
from .templatetags.terms import replace_terms


def TermsProcessor(instance, placeholder, rendered_content, original_context):
    """
    Adds links all placeholders plugins except django-terms plugins
    """
    if 'terms' in original_context:
        return rendered_content

    return mark_safe(replace_terms(rendered_content))
