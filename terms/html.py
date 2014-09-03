# coding: utf-8

from io import StringIO
from lxml.etree import Comment
from lxml.html import tostring, _looks_like_full_html_unicode, parse
try:
    from django.utils.encoding import force_text
except ImportError:  # For Django < 1.4.2
    from django.utils.encoding import force_unicode as force_text
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


def get_translate_function(replace_dict, variants_dict):
    def translate(match):
        before, name = match.group('before', 'name')

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
        return before + replaced_name
    return translate


def is_valid_node(node):
    if node.tag is Comment or node.tag in TERMS_IGNORED_TAGS \
            or node.get('id') in TERMS_IGNORED_IDS:
        return False
    classes = frozenset(node.get('class', '').split())
    return classes.isdisjoint(TERMS_IGNORED_CLASSES)


def get_text(node):
    text = node.text or ''
    for subnode in node.getchildren():
        text += subnode.tail or ''
    return text.replace('&', '&amp;')


def get_interesting_contents(parent_node, replace_regexp):
    if is_valid_node(parent_node):

        text = get_text(parent_node)
        if text and replace_regexp.search(text):
            yield parent_node

        for node in parent_node.getchildren():
            for subnode in get_interesting_contents(node, replace_regexp):
                yield subnode


if TERMS_ENABLED:
    def replace_terms(html):
        html = force_text(html)
        remove_body = False
        remove_p = False
        etree = parse(StringIO(html))
        root_node = etree.getroot()
        if not _looks_like_full_html_unicode(html):
            root_node = root_node.getchildren()[0]
            remove_body = True
            if root_node.getchildren()[0].tag == 'p' and html[:3] != '<p>':
                remove_p = True

        variants_dict = Term.objects.variants_dict()
        replace_dict = Term.objects.replace_dict()
        replace_regexp = Term.objects.replace_regexp()
        replace_regexp__sub = replace_regexp.sub
        translate = get_translate_function(replace_dict, variants_dict)

        for node in get_interesting_contents(root_node, replace_regexp):
            new_content = replace_regexp__sub(
                translate, tostring(node, encoding='unicode'))
            new_node = parse(StringIO(new_content)).getroot().getchildren()[0]
            if node.tag != 'body':
                new_node = new_node.getchildren()[0]
            node.getparent().replace(node, new_node)

        if remove_body:
            if remove_p:
                root_node = root_node.getchildren()[0]
            out = root_node.text or ''
            out += ''.join([tostring(node, encoding='unicode')
                            for node in root_node.getchildren()])
            return out
        return tostring(etree, encoding='unicode')
else:
    def replace_terms(html):
        return html
