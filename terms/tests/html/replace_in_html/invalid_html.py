import os.path
from unittest import TestCase
from terms.html import replace_in_html

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


class InvalidHTMLTestCase(TestCase):
    def test_start_tag(self):
        """
        After being reconstructed, invalid missing start tags should be
        stripped.
        """
        filename = 'valid.html'
        valid = open(os.path.join(CURRENT_PATH, filename)).read()
        filename = 'missing_start_tag.html'
        invalid = open(os.path.join(CURRENT_PATH, filename)).read()

        new_html = replace_in_html(invalid).prettify()
        self.assertEqual(valid, new_html)

    def test_end_tag(self):
        """
        After being reconstructed, invalid missing end tags should be there.
        """
        filename = 'valid.html'
        valid = open(os.path.join(CURRENT_PATH, filename)).read()
        filename = 'missing_end_tag.html'
        invalid = open(os.path.join(CURRENT_PATH, filename)).read()

        new_html = replace_in_html(invalid).prettify()
        self.assertEqual(valid, new_html)

    def test_start_end_tag(self):
        """
        After being reconstructed, invalid start-end tags should be valid.
        """
        filename = 'valid.html'
        valid = open(os.path.join(CURRENT_PATH, filename)).read()
        filename = 'invalid_start-end_tag.html'
        invalid = open(os.path.join(CURRENT_PATH, filename)).read()

        new_html = replace_in_html(invalid).prettify()
        self.assertEqual(valid, new_html)
