# coding: utf-8

from __future__ import unicode_literals
import os.path
from django.test import TestCase
from terms.html import replace_terms
from terms.models import Term


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    return open(os.path.join(CURRENT_PATH, filename)).read()


class ValidHTMLTestCase(TestCase):
    def testEmptyString(self):
        self.assertHTMLEqual(replace_terms(''), '')

    def test(self):
        """
        After being reconstructed, valid_html should be exactly the same.
        And after being reconstructed, valid_html_with_extra_spaces should
        be exactly the same as valid_html (since extra whitespaces within tags
        are stripped).
        """
        html = read_file('valid_html.html')
        html_w_extra_spaces = read_file('valid_html_with_extra_spaces.html')

        new_html = replace_terms(html)
        self.assertHTMLEqual(html, new_html)

        new_html_w_extra_spaces = replace_terms(html_w_extra_spaces)
        self.assertHTMLEqual(html, new_html_w_extra_spaces)

    def testUnicode(self):
        Term.objects.create(name='était', url='github.com')

        control = 'Il <a href="github.com">était</a> une fois…'

        text = 'Il était une fois…'
        self.assertEqual(replace_terms(text), control)

        html = 'Il &eacute;tait une fois&hellip;'
        self.assertEqual(replace_terms(html), control)
