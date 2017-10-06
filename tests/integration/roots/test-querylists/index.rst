============
Test Queries
============

.. homepage::

    in_nav: False

Content after title.

.. querylist::

    template: querylist.html
    queries:
        - label: Recent Blog Posts
          style: primary
          query:
              kbtype: section
              limit: 5
        - label: Recent Articles
          style: info
          query:
              kbtype: article
              limit: 5
        - label: Recent Tutorials
          style: warning
          query:
              kbtype: article
              limit: 5

.. toctree::

    articles/index