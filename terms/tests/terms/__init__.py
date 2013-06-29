import os
from django.template import Template, Context
from django.test import TestCase
from terms.templatetags.terms import replace_terms
from terms.models import Term


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def read_file(filename, context=None):
    if context is None:
        context = {}
    context = Context(context)
    return Template(
        open(os.path.join(CURRENT_PATH, filename)).read()
    ).render(context)


class TermsTestCase(TestCase):
    templates = [
        ('1_before.html', '1_after.html'),
        ('2_before.html', '2_after.html'),
    ]

    def setUp(self):
        self.term1 = Term.objects.create(
            name='complicated term', url='http://en.wiktionary.org/wiki/term')
        self.term2 = Term.objects.create(
            name='indricothere',
            definition='A nice mix between a rhino and a giraffe.')

    def assertDetailView(self, term, status_code=200):
        response = self.client.get(term.get_absolute_url())
        self.assertEqual(response.status_code, status_code)

    def assertCachedRegex(self):
        """
        Checks if adding links hits the database.

        The database should be hit during the first replacement after a change
        in the terms table.  After that, a regular expression is cached to
        avoid hitting the database.
        """
        with self.assertNumQueries(0):
            for before_template, after_template in self.templates:
                replace_terms(read_file(before_template))

    def test1(self):
        self.assertHTMLEqual(
            replace_terms(read_file('1_before.html')),
            read_file('1_after.html', {'term': self.term1}))
        self.assertDetailView(self.term1, status_code=404)

        self.assertCachedRegex()

    def test2(self):
        self.assertHTMLEqual(
            replace_terms(read_file('2_before.html')),
            read_file('2_after.html', {'term': self.term2}))
        self.assertDetailView(self.term2)

        self.assertCachedRegex()
