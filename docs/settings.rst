.. _settings:

Settings
========

.. _Common settings:

Common settings
---------------

.. _TERMS_ENABLED:

TERMS_ENABLED
.............

:Default: ``True``
:Definition: If set to ``False``, globally disabled django-terms.

.. _TERMS_DEBUG:

TERMS_DEBUG
...........

:Default: ``DEBUG``
:Definition: If set to ``True``, allows django-terms to raise minor exceptions
             (see :ref:`Exceptions`).

.. _TERMS_REPLACE_FIRST_ONLY:

TERMS_REPLACE_FIRST_ONLY
........................

:Default: ``True``
:Definition: If set to ``True``, adds a link only on the first occurrence
             of each term
:Used by: :ref:`Middleware`, :ref:`Template filter`

.. _TERMS_ADDITIONAL_IGNORED_APPS:

TERMS_ADDITIONAL_IGNORED_APPS
.............................

:Default: ``()``
:Definition: A list or tuple of ignored Django applications
             (expressed as strings)
:Used by: :ref:`Middleware`
:Extends: `TERMS_IGNORED_APPS`_
:Syntax example: ``['cms']``

.. _TERMS_ADDITIONAL_IGNORED_TAGS:

TERMS_ADDITIONAL_IGNORED_TAGS
.............................

:Default: ``()``
:Definition: A list or tuple of ignored HTML tags (expressed as strings)
:Used by: :ref:`Middleware`, :ref:`Template filter`
:Extends: `TERMS_IGNORED_TAGS`_
:Syntax example: ``['h1', 'h2', 'h3', 'footer']``

.. _TERMS_ADDITIONAL_IGNORED_CLASSES:

TERMS_ADDITIONAL_IGNORED_CLASSES
................................

:Default: ``()``
:Definition: A list or tuple of ignored HTML classes (expressed as strings)
:Used by: :ref:`Middleware`, :ref:`Template filter`
:Extends: `TERMS_IGNORED_CLASSES`_
:Syntax example: ``['footnote', 'text-caption']``

.. _TERMS_ADDITIONAL_IGNORED_IDS:

TERMS_ADDITIONAL_IGNORED_IDS
............................

:Default: ``()``
:Definition: A list or tuple of ignored HTML IDs (expressed as strings)
:Used by: :ref:`Middleware`, :ref:`Template filter`
:Extends: `TERMS_IGNORED_IDS`_
:Syntax example: ``['article-footer', 'side-content']``

.. _TERMS_DEFINITION_WIDGET:

TERMS_DEFINITION_WIDGET
.......................

:Default: ``'auto'``
:Definition: Explicitly tells django-terms which text widget to choose
             for the definition of a term.  Accepted values are
             ``'auto'``, ``'basic'``, ``'tinymce'``, and ``'ckeditor'``.


.. _Advanced settings:

Advanced settings
-----------------

These settings should not be used, unless you know perfectly
what you are doing.

TERMS_IGNORED_APPS
..................

:Default: see `terms/settings.py`
:Definition: A list or tuple of ignored Django applications
             (expressed as strings)
:Used by: :ref:`Middleware`

TERMS_IGNORED_TAGS
..................

:Default: see `terms/settings.py`
:Definition: A list or tuple of ignored HTML tags (expressed as strings)
:Used by: :ref:`Middleware`, :ref:`Template filter`

TERMS_IGNORED_CLASSES
.....................

:Default: see `terms/settings.py`
:Definition: A list or tuple of ignored HTML classes (expressed as strings)
:Used by: :ref:`Middleware`, :ref:`Template filter`

TERMS_IGNORED_IDS
.................

:Default: see `terms/settings.py`
:Definition: A list or tuple of ignored HTML IDs (expressed as strings)
:Used by: :ref:`Middleware`, :ref:`Template filter`
