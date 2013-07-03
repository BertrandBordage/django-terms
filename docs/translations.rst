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
