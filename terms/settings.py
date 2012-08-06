from django.conf import settings


TERMS_IGNORED_TAGS = getattr(settings, 'TERMS_IGNORED_TAGS',
    (
        'head',
        'style',
        'script',
        'a',
        'textarea',
        'button',
        'code',
        'samp',
        'kbd',
    )
)
if hasattr(settings, 'TERMS_ADDITIONAL_IGNORED_TAGS'):
    TERMS_IGNORED_TAGS.extend(settings.TERMS_ADDITIONAL_IGNORED_TAGS)

TERMS_IGNORED_CLASSES = frozenset(
    getattr(settings, 'TERMS_IGNORED_CLASSES',
        (
        )
    )
)

TERMS_IGNORED_IDS = getattr(settings, 'TERMS_IGNORED_IDS',
    (
    )
)

TERMS_REPLACE_FIRST_ONLY = getattr(settings, 'TERMS_REPLACE_FIRST_ONLY', True)
