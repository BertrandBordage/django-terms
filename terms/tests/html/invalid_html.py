import os.path
from django.test import TestCase
from terms.html import replace_terms

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    return open(os.path.join(CURRENT_PATH, filename)).read()


class InvalidHTMLTestCase(TestCase):
    def test_start_tag(self):
        """
        After being reconstructed, invalid missing start tags should be
        stripped.
        """
        valid = read_file('valid.html')
        invalid = read_file('missing_start_tag.html')

        new_html = replace_terms(invalid)
        self.assertHTMLEqual(valid, new_html)

    def test_end_tag(self):
        """
        After being reconstructed, invalid missing end tags should be there.
        """
        valid = read_file('valid.html')
        invalid = read_file('missing_end_tag.html')

        new_html = replace_terms(invalid)
        self.assertHTMLEqual(valid, new_html)
