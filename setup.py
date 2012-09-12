#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages


setup(
    name='django-terms',
    version='0.4.7',
    author='Bertrand Bordage',
    author_email='bordage.bertrand@gmail.com',
    url='https://github.com/BertrandBordage/django-terms',
    description='Site-wide adds a definition '
                'or a link for specialized terms.',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    license='BSD',
    packages=find_packages(),
    install_requires=[
        "Django >= 1.4",
    ],
    include_package_data=True,
    zip_safe=False,
)
