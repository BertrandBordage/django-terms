# coding: utf-8

from .html import TermsHTMLReconstructor
from django.core.urlresolvers import resolve, Resolver404
from .settings import TERMS_IGNORED_APPS
from django.conf import settings


class TermsMiddleware:
    def __init__(self):
        self.parser = TermsHTMLReconstructor()

    def process_response(self, request, response):
        url = request.path
        try:
            app_name = resolve(url).app_name
            app_ignored = app_name in TERMS_IGNORED_APPS
        except Resolver404:
            if settings.DEBUG:
                raise Resolver404("could not find whether the application of "
                                  "'%s' is in TERMS_IGNORED_APPS" % url)
            app_ignored = True

        is_html = 'text/html' in response['Content-Type']

        if not app_ignored and is_html:
            try:
                self.parser.feed(response.content.decode('utf-8'))
                response.content = self.parser.out
            finally:
                self.parser.reset()

        return response
