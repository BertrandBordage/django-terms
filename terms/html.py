# coding: utf-8

from HTMLParser import HTMLParser
from .models import Term
from .settings import TERMS_IGNORED_TAGS, TERMS_IGNORED_CLASSES, \
                      TERMS_IGNORED_IDS, TERMS_REPLACE_FIRST_ONLY
from django.conf import settings
from .exceptions import HTMLValidationWarning


class NeutralHTMLReconstructor(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.out = []

    def feed(self, data):
        data = self.unescape(data)
        HTMLParser.feed(self, data)
        self.out = ''.join(self.out)

    def concat_attrs(self, attrs):
        return ''.join(' %s="%s"' % (attr[0], attr[1]) for attr in attrs)

    def handle_startendtag(self, tag, attrs):
        attrs = self.concat_attrs(attrs)
        self.out.append('<%s%s />' % (tag, attrs))

    def handle_starttag(self, tag, attrs):
        attrs = self.concat_attrs(attrs)
        self.out.append('<%s%s>' % (tag, attrs))

    def handle_endtag(self, tag):
        self.out.append('</%s>' % tag)

    def handle_data(self, data):
        self.out.append(data)

    def handle_comment(self, data):
        self.out.append('<!--%s-->' % data)

    def handle_decl(self, decl):
        self.out.append('<!%s>' % decl)

    def handle_pi(self, data):
        self.out.append('<?%s>' % data)

    def unknown_decl(self, decl):
        self.out.append('<![%s]>' % decl)


class TermsHTMLReconstructor(NeutralHTMLReconstructor):
    def reset(self):
        NeutralHTMLReconstructor.reset(self)
        self.tree_level = 0
        self.opened_tags = []
        self.disabled_level = None
        self.replace_dict = Term.objects.replace_dict()
        self.replace_regexp = Term.objects.replace_regexp()

    @property
    def allow_replacements(self):
        return self.disabled_level is None

    def replace_terms(self, html):
        def translate(match):
            before, term, after = match.group('before'), \
                                  match.group('term'), \
                                  match.group('after')
            replaced_term = self.replace_dict.get(term, term)
            if TERMS_REPLACE_FIRST_ONLY and term in self.replace_dict:
                del self.replace_dict[term]
            return before + replaced_term + after

        return self.replace_regexp.sub(translate, html)

    def handle_starttag(self, tag, attrs):
        NeutralHTMLReconstructor.handle_starttag(self, tag, attrs)
        self.opened_tags.append((tag, self.get_starttag_text()))
        self.tree_level += 1

        dict_attrs = dict(attrs)
        has_disabled_tag = tag in TERMS_IGNORED_TAGS
        classes = frozenset(dict_attrs.get('class', '').split())
        has_disabled_class = not classes.isdisjoint(TERMS_IGNORED_CLASSES)
        has_disabled_id = dict_attrs.get('id', '') in TERMS_IGNORED_IDS

        if self.allow_replacements and (has_disabled_tag or has_disabled_class
                                        or has_disabled_id):
            self.disabled_level = self.tree_level

    def handle_endtag(self, tag):
        NeutralHTMLReconstructor.handle_endtag(self, tag)

        opened_tag, full_start_tag = self.opened_tags.pop()
        if tag != opened_tag:
            if settings.DEBUG:
                raise HTMLValidationWarning('unable to find the end tag for '
                                            + full_start_tag)
            self.tree_level -= 1  # We suppose the start tag is a start-end tag
                                  # with its final '/' missing.

        if self.disabled_level and self.disabled_level == self.tree_level:
            self.disabled_level = None

        self.tree_level -= 1

    def handle_data(self, data):
        if self.allow_replacements:
            data = self.replace_terms(data)
        self.out.append(data)
