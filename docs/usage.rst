.. include:: links.rst

.. _Usage:

Usage
=====

#. Add some terms in the admin
#. Choose how django-terms should apply to your website:

   * :ref:`Middleware` (to give django-terms a try or for development)
   * :ref:`Template filter` (for production)
   * :ref:`With django-CMS`

The added terms should now be automatically linked to their definitions.


.. _Middleware:

Middleware
----------

A middleware is available to automatically add links on all your website.
It is not recommended to use it in production because it parses and rebuilds
whole pages, which can be an overkill in most cases (even though django-terms
has excellent performances).

It is also perfect for development: it never fails silently, unlike filters
(see :ref:`Exceptions` for more details).

#. Add ``'terms.middleware.TermsMiddleware',``
   to your ``MIDDLEWARE_CLASSES``
#. If the middleware applies to unwanted Django applications,
   HTML tags, classes, or IDs, set the corresponding :ref:`Common settings`


.. _Template filter:

Template filter
---------------

A template filter is available to add links only on desired parts of
your website.

#. Choose one of your existing templates
#. Add ``{% load terms %}`` to the beginning of the file (just after
   ``{% extends '[file]' %}`` if you have one)
#. Use the filter ``replace_terms`` like every normal filter
#. If the filter applies to unwanted HTML tags, classes, or IDs,
   set the corresponding `:ref:Common settings`

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
   Go to :ref:`Common settings`, and you will find the solution:

     Add this line in `settings.py`::

       TERMS_ADDITIONAL_IGNORED_CLASSES = ['code-snippet']


.. _With django-CMS:

With django-CMS
---------------

A few tools are available to make your life easier if you use `django-CMS`_.

.. _Plugin processor:

Plugin processor
................

It will automatically apply the :ref:`template filter` on every plugin.

To use it, add or modify ``CMS_PLUGIN_PROCESSORS`` in `settings.py`::

   CMS_PLUGIN_PROCESSORS = (
       ...
       'terms.cms_plugin_processors.TermsProcessor',
       ...
   )

.. _Glossary plugin:

Glossary plugin
...............

This plugin displays all terms and their definitions.

Don't forget to update ``CMS_PLACEHOLDER_CONF`` in your `settings.py`
if you defined it, otherwise this plugin will not be available from your
placeholders.

Apart from this, nothing to do to make it work.

.. _App hook and menu:

App hook and menu
.................

You can use the the app hook and the menu to integrate the complete glossary
to your CMS architecture.

Nothing to do to make it work.
