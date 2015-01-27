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
    def setUp(self):
        self.term = Term.objects.create(name='était', url='github.com')

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
        control = 'Il <a href="github.com">était</a> une fois…'

        text = 'Il était une fois…'
        self.assertEqual(replace_terms(text), control)

        html = 'Il &eacute;tait une fois&hellip;'
        self.assertEqual(replace_terms(html), control)

    def testText(self):
        self.assertHTMLEqual(replace_terms('était'),
                             '<a href="github.com">était</a>')

    def testTextAndNode(self):
        self.assertHTMLEqual(replace_terms('était <em>une fois</em>'),
                             '<a href="github.com">était</a> <em>une fois</em>')

    def testSingleParagraph(self):
        self.assertHTMLEqual(replace_terms('<p>était</p>'),
                             '<p><a href="github.com">était</a></p>')

    def testSingleAttributedParagraph(self):
        self.assertHTMLEqual(replace_terms('<p id="test">était</p>'),
                             '<p id="test"><a href="github.com">était</a></p>')

    def testMultipleParagraphs(self):
        html = ('<p>First paragraph</p>'
                '<p>Il était une fois</p>')
        control = ('<p>First paragraph</p>'
                   '<p>Il <a href="github.com">était</a> une fois</p>')
        self.assertHTMLEqual(replace_terms(html), control)

    def testMultipleAttributedParagraphs(self):
        html = (
            '<p id="test1">First paragraph</p>'
            '<p id="test2">Il était une fois</p>')
        control = (
            '<p id="test1">First paragraph</p>'
            '<p id="test2">Il <a href="github.com">était</a> une fois</p>')
        self.assertHTMLEqual(replace_terms(html), control)
