************
django-terms
************

Site-wide adds a definition or a link for specialized terms.

.. contents::
   :depth: 2



Requirements
============

Mandatory
---------

* `Django <https://www.djangoproject.com/>`_ (tested with 1.4).


Optional
--------

* `django-ckeditor <https://github.com/shaunsephton/django-ckeditor>`_
  (tested with 3.6.2.1) to type the definition in a beautiful GUI;
* `django-reversion <https://github.com/etianen/django-reversion>`_
  (tested with 1.6.0) to recover changes and deletions;
* `django-CMS <https://www.django-cms.org/>`_ (tested with 2.3),
  because django-terms has an apphook and a menu.



Installation
============

#. ``[sudo] pip install django-terms``;
#. Add ``'terms',`` to your ``INSTALLED_APPS``;
#. Add terms to your urls:
    * add ``url(r'^terms/', include('terms.urls')),`` to your ``urls.py``;
    * or, if you are using django-CMS, add a page and use the apphook and menu.



Usage
=====

#. Add some terms in the admin;
#. Choose how django-terms should apply to your website:
   `Global use`_ (recommended to give django-terms a try) or
   `Local use`_ (recommended for production).

The added terms should now be automatically linked to their definitions.


Global use
----------

A middleware is available to automatically add links on all your website.
It is not recommended to use it, since it will add links in all your
applications, including django.contrib.admin.  But since it only requires one
line of change, it is a perfect way to start using django-terms.

#. Just add ``'terms.middleware.TermsMiddleware',``
   to your ``MIDDLEWARE_CLASSES``.


Local use
---------

A template filter is available to add links only on desired parts of
your website.

#. Choose one of your existing templates;
#. Add ``{% load terms %}`` to the beginning of the file (just after
   ``{% extends '[file]' %}`` if you have one);
#. Use the filter ``replace_terms`` like every normal filter.

Example:

::

    {% extends 'base.html' %}
    {% load terms %}

    {% block article_header %}
      {{ article.header|replace_terms }}
    {% endblock %}
    {% block article_content %}
      {% filter replace_terms %}
        {{ article.section1 }}
        {{ article.section2 }}
      {% endfilter %}
    {% endblock %}



Settings
========

Common settings
---------------

``TERMS_ADDITIONAL_IGNORED_APPS``
    | Default: ``()``
    | A list or tuple of ignored Django apps (expressed as strings).
      This setting extends ``TERMS_IGNORED_APPS``
      (see `Advanced settings`_).

``TERMS_ADDITIONAL_IGNORED_TAGS``
    | Default: ``()``
    | A list or tuple of ignored HTML tags (expressed as strings).
      This setting extends ``TERMS_IGNORED_TAGS``
      (see `Advanced settings`_).

``TERMS_ADDITIONAL_IGNORED_CLASSES``
    | Default: ``()``
    | A list or tuple of ignored HTML classes (expressed as strings).
      This setting extends ``TERMS_IGNORED_CLASSES``
      (see `Advanced settings`_).

``TERMS_ADDITIONAL_IGNORED_IDS``
    | Default: ``()``
    | A list or tuple of ignored HTML IDs (expressed as strings).
      This setting extends ``TERMS_IGNORED_IDS``
      (see `Advanced settings`_).

``TERMS_REPLACE_FIRST_ONLY``
    | Default: ``True``
    | If set to True, add a link only on the first occurrence of each term.

``TERMS_CACHE_TIMEOUT``
    | Default: ``30``
    | Cache timeout of django-terms (in seconds).


Advanced settings
-----------------

``TERMS_IGNORED_APPS``
    | Default: see ``terms/settings.py``
    | A list or tuple of ignored Django apps (expressed as strings).

``TERMS_IGNORED_TAGS``
    | Default: see ``terms/settings.py``
    | A list or tuple of ignored HTML tags (expressed as strings).
      This is already set, so you should use ``TERMS_ADDITIONAL_IGNORED_TAGS``
      (see `Common settings`_) if you do not want to break
      the default behavior.

``TERMS_IGNORED_CLASSES``
    | Default: see ``terms/settings.py``
    | A list or tuple of ignored HTML classes (expressed as strings).

``TERMS_IGNORED_IDS``
    | Default: see ``terms/settings.py``
    | A list or tuple of ignored HTML IDs (expressed as strings).



Side effects
============

Why?
----

When using django-terms, your HTML pages are totally or partially
reconstructed:

* totally reconstructed if you use the middleware (see `Global Use`_);
* partially reconstructed if you use the filter (see `Local Use`_).

The content is parsed with
`HTMLParser <http://docs.python.org/library/htmlparser.html>`_,
then rebuilt.  See ``NeutralHTMLReconstructor`` and ``TermsHTMLReconstructor``
in `tems/html.py` to understand exactly how it is rebuilt.


List of known side effects
--------------------------

A few side effects are therefore happening during HTML reconstruction:

* Entity names and numbers (e.g. ``&eacute;``, ``&#233;``, …) are unescaped.
  This means they are replaced with their unicode characters
  (e.g. ``&eacute;`` -> ``é``);
* Additional spaces inside HTML tags are stripped:
    * Start tags ``<a  href = "url" >``
      -> ``<a href="url">``;
    * End tags ``</ a >``
      -> ``</a>``;
    * “Start-end” tags ``<input  style = "text"  />``
      -> ``<input style="text" />``.

.. warning::
   This implies one bad side effect: the unescaping breaks the special
   characters rendering in some complex form fields like
   `django-ckeditor`_.  `django.contrib.admin` is already ignored,
   so you should not encounter any problem.  Otherwise, using filters
   instead of the middleware and/or ignore the correct
   apps/tags/classes/ids using `Common settings`_ will ensure a proper
   rendering.



Translations
============

Status
------

.. image::
   https://www.transifex.com/projects/p/django-terms/resource/core/chart/image_png

Write your translation
----------------------

Localization is done directly on
`our Transifex page <https://www.transifex.com/projects/p/django-terms/>`_.
Ask for a new language, and you'll get it ready for translation
within a couple of days.


Compile it
----------

First, you need to get it from Transifex, then to compile it:

#. Make sure you have
   `transifex-client <http://pypi.python.org/pypi/transifex-client/>`_
   installed: ``[sudo] pip install transifex-client``;
#. Pull your translation: ``tx pull -l [lang]``;
#. Compile it:
   ``msgfmt terms/locale/[lang]/LC_MESSAGES/django.po
   -o terms/locale/[lang]/LC_MESSAGES/django.mo``.
