Articles
========

.. resource:: section

    style: 'is-bold is-info'
    in_nav: True
    weight: 10

A list of articles is here.

.. querylist::

    template: querylist.html
    queries:
        - label: Recent Sections
          rtype: section
          limit: 5
        - label: Recent Articles
          rtype: article
          limit: 5


.. toctree::
    :maxdepth: 1
    :caption: Contents:

    first_article