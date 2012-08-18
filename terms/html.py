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
        self.variants_dict = Term.objects.variants_dict()
        self.replace_dict = Term.objects.replace_dict()
        self.replace_regexp = Term.objects.replace_regexp()

    @property
    def allow_replacements(self):
        return self.disabled_level is None

    def replace_terms(self, html):
        def translate(match):
            before, name, after = match.group('before'), \
                                  match.group('name'), \
                                  match.group('after')
            replaced_name = self.replace_dict.get(name, name)
            if TERMS_REPLACE_FIRST_ONLY and name in self.replace_dict:
                for variant in self.variants_dict[name]:
                    del self.replace_dict[variant]
            return before + replaced_name + after

        return self.replace_regexp.sub(translate, html)

    def handle_starttag(self, tag, attrs):
        NeutralHTMLReconstructor.handle_starttag(self, tag, attrs)
        self.opened_tags.append((tag, self.get_starttag_text(), self.getpos()))
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
        try:
            opened_tag, full_start_tag, pos = self.opened_tags.pop()
            # Adds the tag to HTML only if it has a start tag.
            NeutralHTMLReconstructor.handle_endtag(self, tag)
        except IndexError:
            if settings.DEBUG:
                lines = self.rawdata.split('\n')
                line = self.getpos()[0]
                lines = '\n'.join(lines[line - 2:line])
                raise HTMLValidationWarning('unable to find the start tag '
                                            'for </%s> in:\n\n%s'
                                            % (tag, lines))
            return None
        if tag != opened_tag:
            if settings.DEBUG:
                lines = self.rawdata.split('\n')
                start_line, end_line = pos[0], self.getpos()[0]
                lines = '\n'.join(lines[start_line - 1:end_line])
                raise HTMLValidationWarning('unable to find the end tag '
                                            'for %s in:\n\n%s'
                                            % (full_start_tag, lines))
            self.tree_level -= 1  # We suppose the start tag is a start-end tag
                                  # with its final '/' missing.

        if self.disabled_level and self.disabled_level == self.tree_level:
            self.disabled_level = None

        self.tree_level -= 1

    def handle_data(self, data):
        if self.allow_replacements:
            data = self.replace_terms(data)
        self.out.append(data)
