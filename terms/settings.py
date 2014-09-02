# coding: utf-8

from django.conf import settings


#
# General settings
#


TERMS_ENABLED = getattr(settings, 'TERMS_ENABLED', True)

TERMS_DEBUG = getattr(settings, 'TERMS_DEBUG', settings.DEBUG)

TERMS_REPLACE_FIRST_ONLY = getattr(settings, 'TERMS_REPLACE_FIRST_ONLY', True)


#
# Settings to specify where django-terms should not replace terms
#


TERMS_IGNORED_APPS = getattr(settings, 'TERMS_IGNORED_APPS',
    [
        'admin',
        'admindocs',
    ]
)
if hasattr(settings, 'TERMS_ADDITIONAL_IGNORED_APPS'):
    TERMS_IGNORED_APPS.extend(settings.TERMS_ADDITIONAL_IGNORED_APPS)
TERMS_IGNORED_APPS = frozenset(TERMS_IGNORED_APPS)


TERMS_IGNORED_TAGS = getattr(settings, 'TERMS_IGNORED_TAGS',
    [
        'head',
        'style',
        'script',
        'a',
        'textarea',
        'button',
        'code',
        'samp',
        'kbd',
    ]
)
if hasattr(settings, 'TERMS_ADDITIONAL_IGNORED_TAGS'):
    TERMS_IGNORED_TAGS.extend(settings.TERMS_ADDITIONAL_IGNORED_TAGS)
TERMS_IGNORED_TAGS = frozenset(TERMS_IGNORED_TAGS)


TERMS_IGNORED_CLASSES = getattr(settings, 'TERMS_IGNORED_CLASSES',
    [
        'cms_reset',
    ]
)
if hasattr(settings, 'TERMS_ADDITIONAL_IGNORED_CLASSES'):
    TERMS_IGNORED_CLASSES.extend(settings.TERMS_ADDITIONAL_IGNORED_CLASSES)
TERMS_IGNORED_CLASSES = frozenset(TERMS_IGNORED_CLASSES)


TERMS_IGNORED_IDS = getattr(settings, 'TERMS_IGNORED_IDS',
    [
    ]
)
if hasattr(settings, 'TERMS_ADDITIONAL_IGNORED_IDS'):
    TERMS_IGNORED_IDS.extend(settings.TERMS_ADDITIONAL_IGNORED_IDS)
TERMS_IGNORED_IDS = frozenset(TERMS_IGNORED_IDS)


#
# Admin settings
#


AVAILABLE_WIDGETS = ('auto', 'basic', 'tinymce', 'ckeditor')
TERMS_DEFINITION_WIDGET = getattr(settings, 'TERMS_DEFINITION_WIDGET', 'auto')
if TERMS_DEFINITION_WIDGET not in AVAILABLE_WIDGETS:
    raise Exception("unknown value '%s' for TERMS_DEFINITION_WIDGET "
                    "(choices are '%s')" % (TERMS_DEFINITION_WIDGET,
                                            "', '".join(AVAILABLE_WIDGETS)))
