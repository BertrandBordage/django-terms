# coding: utf-8

from .html import TermsHTMLReconstructor
from django.core.urlresolvers import resolve
from .settings import TERMS_IGNORED_APPS


class TermsMiddleware:
    def __init__(self):
        self.parser = TermsHTMLReconstructor()

    def process_response(self, request, response):
        ignored = resolve(request.path).app_name in TERMS_IGNORED_APPS
        is_html = 'text/html' in response['Content-Type']
        if not ignored and is_html:
            self.parser.feed(response.content.decode('utf-8'))
            response.content = self.parser.out
            self.parser.reset()
        return response
