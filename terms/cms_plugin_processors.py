# coding: utf-8

from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from .html import replace_in_html


def TermsProcessor(instance, placeholder, rendered_content, original_context):
    """
    Adds links all placeholders plugins except django-terms plugins
    """
    if 'terms' in original_context:
        return rendered_content

    return mark_safe(force_text(replace_in_html(rendered_content)))
