Kaybee: Knowledge Base for Static Sites
=======================================

.. homepage::

    in_nav: False
    published: 2009-10-21 12:23
    heading: Kaybee
    subheading: Knowledge Base for Static Sites



.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Contents:

    about
    blog/index
    articles/index
    features
    categories/index

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
