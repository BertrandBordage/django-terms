# coding: utf-8

import re
from bs4 import BeautifulSoup
try:
    from django.utils.encoding import smart_text
except ImportError:  # For Django < 1.4.2
    from django.utils.encoding import smart_unicode as smart_text
from .models import Term
from .settings import (
    TERMS_IGNORED_TAGS, TERMS_IGNORED_CLASSES, TERMS_IGNORED_IDS,
    TERMS_REPLACE_FIRST_ONLY, TERMS_ENABLED)


def build_or_regexp(l):
    return re.compile(r'^(?:%s)$' % '|'.join(l))


TAGS_REGEXP = build_or_regexp(TERMS_IGNORED_TAGS)
CLASSES_REGEXP = build_or_regexp(TERMS_IGNORED_CLASSES)
IDS_REGEXP = build_or_regexp(TERMS_IGNORED_IDS)


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


def get_interesting_contents(parent_tag, replace_regexp):
    return [tag for tag in parent_tag.find_all(text=replace_regexp)
            if not (tag.find_parents(TAGS_REGEXP)
                    or tag.find_parents(class_=CLASSES_REGEXP)
                    or tag.find_parents(id=IDS_REGEXP))]


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

        for content in get_interesting_contents(soup, replace_regexp):
            new_content = str_to_soup(replace_terms(
                replace_dict, variants_dict, replace_regexp__sub, content))
            content.replace_with(new_content)

        return smart_text(soup)
else:
    def replace_in_html(html):
        return html
