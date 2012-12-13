#!/usr/bin/env python
#-*- coding:utf-8 -*-

from .html import TermsHTMLReconstructor
from django.template import Context, Template


def TermsProcessor(instance, placeholder, rendered_content, original_context):
    """
    This processor mark all terms in all placeholders plugins except termsplugins
    """
    if 'terms' in original_context:
        return rendered_content
    
    # fix <br> "can't find end tag" error
    rendered_content = re.sub('<br>','<br/>',rendered_content)

    parser = TermsHTMLReconstructor()
    parser.feed(rendered_content)

    t = Template('{{ content|safe }}')
    c = Context({
        'content': parser.out,
    })
    return t.render(c)
