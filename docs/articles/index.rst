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
        - rtype: section
          limit: 5
        - rtype: article
          limit: 5


.. toctree::
    :maxdepth: 1
    :caption: Contents:

    first_article