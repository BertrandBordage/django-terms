# coding: utf-8

from .html import TermsHTMLReconstructor


class TermsMiddleware:
    def __init__(self):
        self.parser = TermsHTMLReconstructor()

    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            self.parser.feed(response.content.decode('utf-8'))
            response.content = self.parser.out
            self.parser.reset()
        return response
