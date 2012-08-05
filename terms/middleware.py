# coding: utf-8

from .utils import NeutralHTMLReconstructor
from .models import Term


class TermsHTMLReconstructor(NeutralHTMLReconstructor):
    def reset(self):
        NeutralHTMLReconstructor.reset(self)
        self.replace_dict = Term.objects.replace_dict()
        self.replace_regexp = Term.objects.replace_regexp()

    def replace(self, text):
        def translate(match):
            try:
                return self.replace_dict[match.group(0)]
            except KeyError:
                pass

        return self.replace_regexp.sub(translate, text)

    def handle_data(self, data):
        data = self.replace(data)
        self.out.append(data)


class TermsMiddleware:
    def __init__(self):
        self.parser = TermsHTMLReconstructor()

    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            self.parser.feed(response.content.decode('utf-8'))
            response.content = ''.join(self.parser.out)
            self.parser.reset()
        return response
