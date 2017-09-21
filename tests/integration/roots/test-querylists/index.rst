============
Test Queries
============

.. resource:: homepage

    in_nav: False

Content after title.

.. querylist::

    template: querylist.html
    queries:
        - label: Recent Blog Posts
          style: primary
          rtype: section
          limit: 5
        - label: Recent Articles
          style: info
          rtype: article
          limit: 5
        - label: Recent Tutorials
          style: warning
          rtype: article
          limit: 5

.. toctree::

    articles/index