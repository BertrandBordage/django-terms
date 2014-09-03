.. include:: links.rst

.. _Requirements:

Requirements
============

.. _Mandatory:

Mandatory
---------

* `Python`_ 2.6, 2.7, 3.2, 3.3 or 3.4
* `Django`_ 1.4, 1.5 or 1.6
* `lxml`_


.. _Optional:

Optional
--------

* `django-tinymce`_ (tested with 1.5.1b2) to type the definition in
  a beautiful GUI (see :ref:`TERMS_DEFINITION_WIDGET`)
* `django-ckeditor`_ (tested with 3.6.2.1) to type the definition in
  another beautiful GUI (see :ref:`TERMS_DEFINITION_WIDGET`)
* `django-reversion`_ (tested with 1.6.0) to recover changes and deletions
* `django-CMS`_ (tested with 2.3)
  because django-terms has an apphook, a menu, a plugin processor and
  a plugin
* `django-haystack`_ (tested with 1.2.7 and 2.1.0)
  because django-terms has a search index
* `django.contrib.sitemaps`_ because django-terms has a sitemap
* `South`_ (tested with 0.8.1) because
  django-terms has migrations
