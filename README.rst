************
django-terms
************

Site-wide adds a definition or a link for specialized terms.

|travis|_
|coveralls|_

.. |travis| image:: https://travis-ci.org/BertrandBordage/django-terms.png
.. _travis: https://travis-ci.org/BertrandBordage/django-terms

.. |coveralls| image:: https://coveralls.io/repos/BertrandBordage/django-terms/badge.png
.. _coveralls: https://coveralls.io/r/BertrandBordage/django-terms


.. image:: https://raw.github.com/BertrandBordage/django-terms/master/example_project/screenshot.png


.. contents::
   :depth: 3



Requirements
============

Mandatory
---------

* `Python <http://python.org/>`_ 2.6, 2.7, 3.2, or 3.3
* `Django <https://www.djangoproject.com/>`_ 1.4 or 1.5
* `beautifulsoup4 <http://www.crummy.com/software/BeautifulSoup/>`_


Optional
--------

* `django-tinymce <https://github.com/aljosa/django-tinymce>`_
  (tested with 1.5.1b2) to type the definition in a beautiful GUI
  (see `TERMS_DEFINITION_WIDGET`_)
* `django-ckeditor <https://github.com/shaunsephton/django-ckeditor>`_
  (tested with 3.6.2.1) to type the definition in another beautiful GUI
  (see `TERMS_DEFINITION_WIDGET`_)
* `django-reversion <https://github.com/etianen/django-reversion>`_
  (tested with 1.6.0) to recover changes and deletions
* `django-CMS <https://www.django-cms.org/>`_ (tested with 2.3)
  because django-terms has an apphook, a menu, a plugin processor and
  a plugin
* `django-haystack <http://haystacksearch.org/>`_ (tested with 1.2.7)
  because django-terms has a search index
* `django.contrib.sitemaps
  <https://docs.djangoproject.com/en/1.4/ref/contrib/sitemaps/>`_
  because django-terms has a sitemap
* `South <http://south.aeracode.org/>`_ (tested with 0.8.1) because
  django-terms has migrations



Installation
============

#. ``[sudo] pip install django-terms``
#. Add ``'terms',`` to your ``INSTALLED_APPS``
#. ``./manage.py syncdb`` (``./manage.py migrate terms`` if you use `South`_)
#. Add terms to your urls:

   * add ``url(r'^terms/', include('terms.urls')),`` to your `urls.py`
   * or, if you are using django-CMS, add a page and use the apphook and menu



Usage
=====

#. Add some terms in the admin
#. Choose how django-terms should apply to your website:

   * `Middleware`_ (to give django-terms a try or for development)
   * `Template filter`_ (for production)
   * `With django-CMS`_

The added terms should now be automatically linked to their definitions.


Middleware
----------

A middleware is available to automatically add links on all your website.
It is not recommended to use it in production because it parses and rebuilds
whole pages, which can be an overkill in most cases (even though django-terms
has excellent performances).

It is also perfect for development: it never fails silently, unlike filters
(see `Exceptions`_ for more details).

#. Add ``'terms.middleware.TermsMiddleware',``
   to your ``MIDDLEWARE_CLASSES``
#. If the middleware applies to unwanted Django applications,
   HTML tags, classes, or IDs, set the corresponding `Common settings`_


Template filter
---------------

A template filter is available to add links only on desired parts of
your website.

#. Choose one of your existing templates
#. Add ``{% load terms %}`` to the beginning of the file (just after
   ``{% extends '[file]' %}`` if you have one)
#. Use the filter ``replace_terms`` like every normal filter
#. If the filter applies to unwanted HTML tags, classes, or IDs,
   set the corresponding `Common settings`_

Example:

   Suppose you have such a template:

     ::

        {% extends 'base.html' %}

        {% block article_header %}
          {{ article.header }}
        {% endblock %}

        {% block article_content %}
          {{ article.section1 }}
          {{ article.section2 }}
        {% endblock %}

   Here is how you can modify it:

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

   Now, suppose you have an HTML class ``code-snippet`` in ``article.section2``
   where you do not want to add links on terms.
   Go to `Common settings`_, and you will find the solution:

     Add this line in `settings.py`::

       TERMS_ADDITIONAL_IGNORED_CLASSES = ['code-snippet']


With django-CMS
---------------

A few tools are available to make your life easier if you use `django-CMS`_.

Plugin processor
................

It will automatically apply the `template filter` on every plugin.

To use it, add or modify ``CMS_PLUGIN_PROCESSORS`` in `settings.py`::

   CMS_PLUGIN_PROCESSORS = (
       ...
       'terms.cms_plugin_processors.TermsProcessor',
       ...
   )

Glossary plugin
...............

This plugin displays all terms and their definitions.

Don't forget to update ``CMS_PLACEHOLDER_CONF`` in your `settings.py`
if you defined it, otherwise this plugin will not be available from your
placeholders.

Apart from this, nothing to do to make it work.

App hook and menu
.................

You can use the the app hook and the menu to integrate the complete glossary
to your CMS architecture.

Nothing to do to make it work.



Settings
========

Common settings
---------------

TERMS_DEBUG
...........

:Default: ``DEBUG``
:Definition: If set to ``True``, allows django-terms to raise minor exceptions
             (see `Exceptions`_).

TERMS_ADDITIONAL_IGNORED_APPS
.............................
:Default: ``()``
:Definition: A list or tuple of ignored Django applications
             (expressed as strings)
:Used by: `Middleware`_
:Extends: `TERMS_IGNORED_APPS`_
:Syntax example: ``['cms']``

TERMS_ADDITIONAL_IGNORED_TAGS
.............................

:Default: ``()``
:Definition: A list or tuple of ignored HTML tags (expressed as strings)
:Used by: `Middleware`_, `Template filter`_
:Extends: `TERMS_IGNORED_TAGS`_
:Syntax example: ``['h1', 'h2', 'h3', 'footer']``

TERMS_ADDITIONAL_IGNORED_CLASSES
................................

:Default: ``()``
:Definition: A list or tuple of ignored HTML classes (expressed as strings)
:Used by: `Middleware`_, `Template filter`_
:Extends: `TERMS_IGNORED_CLASSES`_
:Syntax example: ``['footnote', 'text-caption']``

TERMS_ADDITIONAL_IGNORED_IDS
............................

:Default: ``()``
:Definition: A list or tuple of ignored HTML IDs (expressed as strings)
:Used by: `Middleware`_, `Template filter`_
:Extends: `TERMS_IGNORED_IDS`_
:Syntax example: ``['article-footer', 'side-content']``

TERMS_REPLACE_FIRST_ONLY
........................

:Default: ``True``
:Definition: If set to ``True``, adds a link only on the first occurrence
             of each term
:Used by: `Middleware`_, `Template filter`_

TERMS_DEFINITION_WIDGET
.......................

:Default: ``'auto'``
:Definition: Explicitly tells django-terms which text widget to choose
             for the definition of a term.  Accepted values are
             ``'auto'``, ``'basic'``, ``'tinymce'``, and ``'ckeditor'``.


Advanced settings
-----------------

These settings should not be used, unless you know perfectly
what you are doing.

TERMS_IGNORED_APPS
..................

:Default: see `terms/settings.py`
:Definition: A list or tuple of ignored Django applications
             (expressed as strings)
:Used by: `Middleware`_

TERMS_IGNORED_TAGS
..................

:Default: see `terms/settings.py`
:Definition: A list or tuple of ignored HTML tags (expressed as strings)
:Used by: `Middleware`_, `Template filter`_

TERMS_IGNORED_CLASSES
.....................

:Default: see `terms/settings.py`
:Definition: A list or tuple of ignored HTML classes (expressed as strings)
:Used by: `Middleware`_, `Template filter`_

TERMS_IGNORED_IDS
.................

:Default: see `terms/settings.py`
:Definition: A list or tuple of ignored HTML IDs (expressed as strings)
:Used by: `Middleware`_, `Template filter`_



Troubleshooting
===============

Side effects
------------

Why?
....

When using django-terms, your HTML pages are totally or partially
reconstructed:

* totally reconstructed if you use the `middleware`_
* partially reconstructed if you use the `template filter`_
  or `with django-CMS`_

The content is parsed and rebuilt with `beautifulsoup4`_.  See `tems/html.py`
to understand exactly how.

List of known side effects
..........................

A few side effects are therefore happening during HTML reconstruction:

* Entity names and numbers (e.g. ``&eacute;``, ``&#233;``, …) are unescaped.
  This means they are replaced with their unicode characters
  (e.g. ``&eacute;`` -> ``é``)
* Additional spaces inside HTML tags are stripped:

  * Start tags ``<a  href = "url" >``
    -> ``<a href="url">``
  * End tags ``</ a >``
    -> ``</a>``
  * “Start-end” tags ``<input  style = "text"  />``
    -> ``<input style="text"/>``

.. warning::
   This implies one bad side effect: the unescaping breaks the special
   characters rendering in some complex form fields like
   `django-ckeditor`_.  `django.contrib.admin` is already ignored,
   so you should not encounter any problem.  Otherwise, using filters
   instead of the middleware and/or ignore the correct
   apps/tags/classes/ids using `Common settings`_ will ensure a proper
   rendering.


Performance
-----------

.. note::
   I'll talk about speed, since there is no terrible impact on memory, even if
   you only a GB of RAM on your server.

Unfortunately, django-terms has a significant impact on performance,
especially if you use the `middleware`_.  That's why we recommend using the
`template filter`_.

What is important is the number of HTML tags wrapped by the filter or the
middleware.  Then comes the complexity of your HTML tree.  The amount of
flat text, luckily, has no impact.

To give you an idea, `terms/tests/terms/performance_test_before.html`
contains 263 tags and takes 45 ms to be parsed and rebuilt on my computer
with the middleware.  That gives an average of 160 µs per tag.
If you use the template tag only on the content of the page (124 tags), it
takes 28 ms.  Quite slow, but if you cache the part of the template that's
filtered, this issue should be negligible.


Exceptions
----------

Resolver404
...........

:Raised by: `Middleware`_ only.
:Raised in: `TERMS_DEBUG`_ mode.  Otherwise the page is ignored by django-terms.
:Reason: This happens when django-terms is unable to resolve the current
         ``request.path`` to determine whether the application
         of the current page is in `TERMS_IGNORED_APPS`_.
:Encountered: In django-CMS 2.3, when adding a plugin in frontend editing.



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
There is no access restriction, so feel free to spend two minutes translating
django-terms to your language :o)


Get & Compile
-------------

#. Make sure you have
   `transifex-client <http://pypi.python.org/pypi/transifex-client/>`_
   installed: ``[sudo] pip install transifex-client``
#. Pull all translations from Transifex: ``tx pull -a``
#. Compile them: ``cd terms && django-admin.py compilemessages``
