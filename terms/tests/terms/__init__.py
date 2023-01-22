# coding: utf-8

from __future__ import unicode_literals
import os
from timeit import timeit
from django.contrib.auth.models import User
from django.urls import reverse
from django.template import Template, Context
from django.test import TestCase
from terms.html import replace_terms
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
    fixtures = [
        os.path.join(CURRENT_PATH, 'performance_test.json'),
    ]
    templates = [
        ('1_before.html', '1_after.html'),
        ('2_before.html', '2_after.html'),
        ('3_before.html', '3_after.html'),
        ('4_before.html', '4_after.html'),
    ]

    def setUp(self):
        self.term1 = Term.objects.create(
            name='complicated term', url='http://en.wiktionary.org/wiki/term')
        self.term2 = Term.objects.create(
            name='indricothere',
            definition='A nice mix between a rhino and a giraffe.')
        self.term3 = self.term4 = Term.objects.create(
            name='optimiser|optimize|optimise|optimisé|optimized|optimised',
            url='/optimisation')
        self.term5 = Term.objects.create(
            name='Google', case_sensitive=False, url='http://google.com')
        self.term6_1 = Term.objects.create(
            name='Black & White',
            url='http://en.wikipedia.org/wiki/Black_%26_White_(video_game)')
        self.term6_2 = Term.objects.create(
            name='Black & White 2',
            url='http://en.wikipedia.org/wiki/Black_%26_White_2')

        # Taken from https://criminocorpus.org/musee/282/
        self.performance_test_page = read_file('performance_test_before.html')

        self.user = User.objects.create_superuser('test', 'a@b.com', 'test')

    def assertDetailView(self, term, status_code=200):
        self.assertURL(term.get_absolute_url(), status_code=status_code)

    def assertURL(self, url, status_code=200):
        response = self.client.get(url)
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
        """
        Tests regular case, with a complete HTML structure.
        """
        with self.assertNumQueries(1):
            self.assertHTMLEqual(
                replace_terms(read_file('1_before.html')),
                read_file('1_after.html', {'term': self.term1}))
        self.assertDetailView(self.term1, status_code=404)

        self.assertCachedRegex()

    def test2(self):
        """
        Tests links with definitions.
        """
        with self.assertNumQueries(1):
            self.assertHTMLEqual(
                replace_terms(read_file('2_before.html')),
                read_file('2_after.html', {'term': self.term2}))
        self.assertDetailView(self.term2)

        self.assertCachedRegex()

    def test3(self):
        """
        Tests term variants.
        """
        with self.assertNumQueries(1):
            self.assertHTMLEqual(
                replace_terms(read_file('3_before.html')),
                read_file('3_after.html', {'term': self.term3}))
        self.assertDetailView(self.term3, status_code=404)

    def test4(self):
        """
        Tests isolated term without even a single HTML tag.
        """
        with self.assertNumQueries(1):
            self.assertHTMLEqual(
                replace_terms(read_file('4_before.html')),
                read_file('4_after.html', {'term': self.term4}))

    def test5(self):
        """
        Tests case sensitiveness.
        """
        with self.assertNumQueries(1):
            self.assertHTMLEqual(
                replace_terms(read_file('5_before.html')),
                read_file('5_after1.html', {'term': self.term5}))

        self.term5.case_sensitive = True
        self.term5.save()

        self.assertHTMLEqual(
            replace_terms(read_file('5_before.html')),
            read_file('5_after2.html', {'term': self.term5}))

    def test6(self):
        """
        Tests if a term starting with another shorter term is correctly linked.
        """
        with self.assertNumQueries(1):
            self.assertHTMLEqual(
                replace_terms(read_file('6_before.html')),
                read_file('6_after.html', {'bw1': self.term6_1,
                                           'bw2': self.term6_2}))

    def testAdminRendering(self):
        self.client.login(username='test', password='test')
        self.assertURL(
            reverse('admin:terms_term_changelist'))
        for term in Term.objects.all():
            self.assertURL(
                reverse('admin:terms_term_change', args=(term.pk,)))
            self.assertURL(
                reverse('admin:terms_term_delete', args=(term.pk,)))

    def testPerformance(self):
        self.assertHTMLEqual(
            replace_terms(read_file('performance_test_before.html')),
            read_file('performance_test_after.html'))

        # Parsing & rebuilding should take less than 50 ms
        # on this complex page, even if your computer is a bit slow.
        # On my laptop it takes 11 ms.
        self.assertLess(
            timeit("replace_terms(test_page)",
                   setup='test_page = """%s"""\n'
                         'from terms.html import '
                         'replace_terms' % self.performance_test_page,
                   number=100) / 100.0,
            0.05)
