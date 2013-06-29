import os.path
from django.test import TestCase
from terms.templatetags.terms import replace_terms

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    return open(os.path.join(CURRENT_PATH, filename)).read()


class ValidHTMLTestCase(TestCase):
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
