************
django-terms
************

Site-wide adds a description or a link for specialized terms.



Requirements
============

Mandatory
---------

* Django (tested with 1.4)


Optional
--------

* django-reversion
* django-cms (apphook and menu)



Installation
============

#. ``pip install django-terms``
#. Add ``'terms',`` to your ``INSTALLED_APPS``.
#. Add ``'terms.middleware.TermsMiddleware',`` to your ``MIDDLEWARE_CLASSES``.
#. Add terms to your urls:
    * add ``url(r'^terms/', include('cmsplugin_poll.urls')),`` to your ``urls.py`` ;
    * or, if you are using django-CMS, add a page and use the apphook and menu.



Usage
=====

Add some terms in the admin and a link will be automatically added to its
definition.