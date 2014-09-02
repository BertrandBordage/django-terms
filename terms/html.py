# coding: utf-8

from bs4 import BeautifulSoup
try:
    from django.utils.encoding import smart_text
except ImportError:  # For Django < 1.4.2
    from django.utils.encoding import smart_unicode as smart_text
from .models import Term
from .settings import (
    TERMS_IGNORED_TAGS, TERMS_IGNORED_CLASSES, TERMS_IGNORED_IDS,
    TERMS_REPLACE_FIRST_ONLY, TERMS_ENABLED)


if TERMS_REPLACE_FIRST_ONLY:
    def del_other_occurrences(key, replace_dict, variants_dict):
        if key in replace_dict:
            for variant in variants_dict[key]:
                try:
                    del replace_dict[variant.lower()]
                except KeyError:  # Happens when two variants are case
                    pass          # variants of the same word.
else:
    def del_other_occurrences(*args, **kwargs):
        pass


def replace_terms(replace_dict, variants_dict, replace_regexp__sub, html):
    def translate(match):
        before, name, after = match.group('before', 'name', 'after')

        key = name.lower()

        if key in replace_dict:
            replaced_name, case_sensitive = replace_dict.get(key, ('%s', True))
            if case_sensitive and name not in variants_dict[key]:
                replaced_name = name
            else:
                replaced_name %= name
                del_other_occurrences(key, replace_dict, variants_dict)
        else:
            replaced_name = name
        return before + replaced_name + after
    return replace_regexp__sub(translate, html)


def is_ignored_parent(parent_tag):
    classes = frozenset(parent_tag.get('class', ()))
    return (parent_tag.name in TERMS_IGNORED_TAGS
            or not classes.isdisjoint(TERMS_IGNORED_CLASSES)
            or parent_tag.get('id') in TERMS_IGNORED_IDS)


def get_interesting_contents(soup, replace_regexp):
    for tag in soup.find_all(text=replace_regexp):
        if not any(is_ignored_parent(parent) for parent in tag.parents):
            yield tag


def str_to_soup(html):
    # We use html.parser since lxml adds html and body automatically.
    return BeautifulSoup(html, 'html.parser')


if TERMS_ENABLED:
    def replace_in_html(html):
        soup = str_to_soup(html)

        variants_dict = Term.objects.variants_dict()
        replace_dict = Term.objects.replace_dict()
        replace_regexp = Term.objects.replace_regexp()
        replace_regexp__sub = replace_regexp.sub

        for tag in get_interesting_contents(soup, replace_regexp):
            new_tag = str_to_soup(replace_terms(
                replace_dict, variants_dict, replace_regexp__sub, tag))
            tag.replace_with(new_tag)

        return smart_text(soup)
else:
    def replace_in_html(html):
        return html
