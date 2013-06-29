# coding: utf-8

from django.core.urlresolvers import resolve, Resolver404
from django.utils.encoding import smart_text
from .html import replace_in_html
from .settings import TERMS_IGNORED_APPS, TERMS_DEBUG


class TermsMiddleware(object):
    def process_response(self, request, response):
        url = request.path
        try:
            app_name = resolve(url).app_name
            app_ignored = app_name in TERMS_IGNORED_APPS
        except Resolver404:
            if TERMS_DEBUG:
                raise Resolver404("could not find whether the application of "
                                  "'%s' is in TERMS_IGNORED_APPS" % url)
            app_ignored = True

        is_html = 'text/html' in response['Content-Type']

        if not app_ignored and is_html and response.status_code == 200:
            response.content = smart_text(replace_in_html(response.content))

        return response
