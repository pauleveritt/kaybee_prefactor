=========
Article 1
=========

.. article::
    published: 2009-10-21 12:23


Test when no properties are set, what is default behavior. Look in body
for article1-body.

.. querylist::

    template: querylist_custom.html
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

