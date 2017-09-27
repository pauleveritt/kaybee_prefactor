=========
Article 1
=========

.. article::


Test when no properties are set, what is default behavior. Look in body
for article1-body.

.. querylist::

    template: querylist_custom.html
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

