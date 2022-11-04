# -*- coding: utf-8 -*-
import os
import django

DIRNAME = os.path.dirname(__file__)
SITE_ROOT = os.getenv('SRV')


def pytest_configure():
    from django.conf import settings
    settings.configure(
        SITE_ID=0,
        DEBUG=True,
        TESTING=True,
        SOUTH_TEST_MIGRATE=False,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'terms-testing.db',
                # The following settings are not used with sqlite3:
                'USER': '',
                'PASSWORD': '',
                'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
                'PORT': '',  # Set to empty string for default.
            }
        },
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'DIRS': [os.path.join(DIRNAME, 'templates')],  # include test templates
            'OPTIONS': {
                'debug': True,
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.request'
                ]
            }
        }],
        HAYSTACK_CONNECTIONS={
            'default': {
                'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
                'PATH': os.path.join(SITE_ROOT, 'data', 'whoosh_index'),
                'INDEX_NAME': 'default'
            }
        },
        LANGUAGE_CODE='en',
        LANGUAGES=(('en', 'English'),),
        CMS_LANGUAGES={
            1: [{
                'code': 'en',
                'name': 'English',
                'public': True,
            }],
            'default': {
                'fallbacks': ['en'],
                'public': True,
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'django.contrib.sites',
            'treebeard',
            'cms',
            'menus',
            'terms',
        )
    )
    django.setup()
