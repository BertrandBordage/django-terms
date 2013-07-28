.. include:: links.rst

Troubleshooting
===============

Side effects
------------

Why?
....

When using django-terms, your HTML pages are totally or partially
reconstructed:

* totally reconstructed if you use the :ref:`Middleware`
* partially reconstructed if you use the :ref:`Template filter`
  or :ref:`with django-CMS`

The content is parsed and rebuilt with `beautifulsoup4`_.
See :file:`terms/html.py` to understand exactly how.

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
   apps/tags/classes/ids using :ref:`Common settings` will ensure a proper
   rendering.


Performance
-----------

Good news
.........

django-terms nearly never hits the database.  After each change in your terms
table, the database is hit just one time in order to build a regular expression
that's saved into your cache (assuming you
`set up the cache <https://docs.djangoproject.com/en/dev/topics/cache/#setting-up-the-cache>`_).
If you never change your terms and if your cache is never emptied, there will
be zero database hit.

Considering memory, no particular leak has been found.

Bad news
........

Unfortunately, django-terms has a significant impact on speed,
especially if you use the :ref:`Middleware`.  That's why we recommend using the
:ref:`Template filter`.

What is important is the number of HTML tags wrapped by the filter or the
middleware.  Then comes the complexity of your HTML tree.  The amount of
flat text, luckily, has no impact.

To give you an idea, `terms/tests/terms/performance_test_before.html`
contains 263 tags and takes 45 ms to be parsed and rebuilt on my computer
with the middleware.  That gives an average of 160 µs per tag.
If you use the template tag only on the content of the page (124 tags), it
takes 28 ms.  Quite slow, but if you cache the part of the template that's
filtered, this issue should be negligible.


.. _Exceptions:

Exceptions
----------

Resolver404
...........

:Raised by: :ref:`Middleware` only.
:Raised in: :ref:`TERMS_DEBUG` mode.  Otherwise the page is ignored by django-terms.
:Reason: This happens when django-terms is unable to resolve the current
         ``request.path`` to determine whether the application
         of the current page is in :ref:`TERMS_IGNORED_APPS`.
:Encountered: In django-CMS 2.3, when adding a plugin in frontend editing.
