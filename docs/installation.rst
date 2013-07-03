.. include:: links.rst

Installation
============

#. ``[sudo] pip install django-terms``
#. Add ``'terms',`` to your ``INSTALLED_APPS``
#. ``./manage.py syncdb`` (``./manage.py migrate terms`` if you use `South`_)
#. Add terms to your urls:

   * add ``url(r'^terms/', include('terms.urls')),`` to your `urls.py`
   * or, if you are using django-CMS, add a page and use the apphook and menu
