============
Test Queries
============

.. homepage::

    in_nav: False
    published: 2009-10-21 12:23

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