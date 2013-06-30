# coding: utf-8

import re
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from .models import Term
from .settings import TERMS_IGNORED_TAGS, TERMS_IGNORED_CLASSES, \
                      TERMS_IGNORED_IDS, TERMS_REPLACE_FIRST_ONLY


def build_or_regexp(l):
    return re.compile(r'^(?:%s)$' % '|'.join(l))


TAGS_REGEXP = build_or_regexp(TERMS_IGNORED_TAGS)
CLASSES_REGEXP = build_or_regexp(TERMS_IGNORED_CLASSES)
IDS_REGEXP = build_or_regexp(TERMS_IGNORED_IDS)


if TERMS_REPLACE_FIRST_ONLY:
    def del_other_occurrences(name, replace_dict, variants_dict):
        if name in replace_dict:
            for variant in variants_dict[name]:
                del replace_dict[variant]
else:
    def del_other_occurrences(*args, **kwargs):
        pass


def replace_terms(replace_dict, variants_dict, replace_regexp__sub, html):
    def translate(match):
        match__group = match.group
        before = match__group('before')
        name = match__group('name')
        after = match__group('after')

        replaced_name = replace_dict.get(name, name)
        del_other_occurrences(name, replace_dict, variants_dict)
        return before + replaced_name + after
    return replace_regexp__sub(translate, html)


def is_navigable_string(navigable_string):
    return isinstance(navigable_string, NavigableString)


def html_content_iterator(parent_tag, replace_regexp):
    out = []
    for tag in parent_tag.find_all(text=replace_regexp):
        if tag.find_parent(name=TAGS_REGEXP) \
            or tag.find_parent(class_=CLASSES_REGEXP) \
                or tag.find_parent(id=IDS_REGEXP):
            continue
        out.append(tag)
    return out


def str_to_soup(html):
    # We use html.parser since lxml adds html and body automatically.
    return BeautifulSoup(html, 'html.parser')


def replace_in_html(html):
    variants_dict = Term.objects.variants_dict()
    replace_dict = Term.objects.replace_dict()
    replace_regexp = Term.objects.replace_regexp()
    replace_regexp__sub = replace_regexp.sub
    soup = str_to_soup(html)
    for content in html_content_iterator(soup, replace_regexp):
        new_content = str_to_soup(replace_terms(
            replace_dict, variants_dict, replace_regexp__sub, content))
        content.replace_with(new_content)
    return soup
