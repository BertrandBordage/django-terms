#!/usr/bin/env python
# coding: utf-8
import os

from setuptools import setup, find_packages

version = '1.2.2'


setup(
    name='django-terms',
    version=version,
    author='Bertrand Bordage',
    author_email='bordage.bertrand@gmail.com',
    # url='https://github.com/BertrandBordage/django-terms',
    url='https://gitlab.com/norsktest/django-terms',
    description='Site-wide adds a definition '
                'or a link for specialized terms.',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],
    license='BSD',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Django',
        'django-cms',
        'lxml',
        'django-treebeard',
        'django-sekizai',
        'django-haystack',
    ],
    include_package_data=True,
    zip_safe=False,
)
