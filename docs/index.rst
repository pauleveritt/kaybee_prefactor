Kaybee: Knowledge Base for Static Sites
=======================================

.. homepage::

    in_nav: False
    published: 2009-10-21 12:23
    heading: Kaybee
    subheading: Knowledge Base for Static Sites

Write and organize content with pleasure. Kaybee is a static site generator
based on Sphinx that emphasizes good looks, rich interconnections, and
creating your own kinds of documents.

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Contents:

    about
    blog/index
    articles/index
    features/index
    categories/index
    README

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
        - label: All Recent
          style: warning
          query:
              limit: 10
