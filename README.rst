************
django-terms
************

Site-wide adds a definition or a link for specialized terms.



Requirements
============

Mandatory
---------

* ``Django`` (tested with 1.4).


Optional
--------

* ``django-reversion`` (tested with 1.6.0) to recover changes and deletions;
* ``django-CMS`` (tested with 2.3), because django-terms has an apphook and
  a menu.



Installation
============

#. ``pip install django-terms``;
#. Add ``'terms',`` to your ``INSTALLED_APPS``;
#. Add terms to your urls:
    * add ``url(r'^terms/', include('cmsplugin_poll.urls')),``
      to your ``urls.py``;
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

``TERMS_ADDITIONAL_IGNORED_TAGS``
    **Default: ()** A list or tuple of HTML tags (expressed as strings)
    ignored by django-terms.  This setting extends ``TERMS_IGNORED_TAGS``
    (see `Advanced settings`_)

``TERMS_IGNORED_CLASSES``
    **Default: ()** A list or tuple of HTML classes (expressed as strings)
    ignored by django-terms.

``TERMS_IGNORED_IDS``
    **Default: ()** A list or tuple of HTML IDs (expressed as strings)
    ignored by django-terms.

``TERMS_REPLACE_FIRST_ONLY``
    **Default: True** If set to True, add a link only on the first
    occurrence of each term.


Advanced settings
-----------------

``TERMS_IGNORED_TAGS``
    **Default: see settings.py** A list or tuple of HTML tags (expressed as
    strings) ignored by django-terms.  This is already set, so you should use
    ``TERMS_ADDITIONAL_IGNORED_TAGS`` (see `Common settings`_) if you do not
    want to break the default behavior.
