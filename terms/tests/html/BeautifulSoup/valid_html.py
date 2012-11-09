import os.path
from unittest import TestCase
from terms.html import replace_in_html

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


class ValidHTMLTestCase(TestCase):
    def test(self):
        """
        After being reconstructed, valid_html should be exactly the same.
        And after being reconstructed, valid_html_with_extra_spaces should
        be exactly the same as valid_html (since extra whitespaces within tags
        are stripped).
        """
        filename = 'valid_html.html'
        html = open(os.path.join(CURRENT_PATH, filename)).read()
        filename = 'valid_html_with_extra_spaces.html'
        html_w_extra_spaces = open(os.path.join(CURRENT_PATH, filename)).read()

        new_html = replace_in_html(html).prettify()
        self.assertEqual(html, new_html)

        new_html_w_extra_spaces = replace_in_html(html_w_extra_spaces).prettify()
        self.assertEqual(html, new_html_w_extra_spaces)
