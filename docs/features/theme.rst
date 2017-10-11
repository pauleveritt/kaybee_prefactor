==============
Theme Features
==============

.. article::
    published: 2017-10-01 00:00
    synopsis:
        The templating and CSS features for Kaybee, in detail.


- A resource can specify a template in YAML, inherit it from the section,
  or fall back on getting it from the class name.

- The template file named can be come from the ``_templates`` directory
  in the conf directory, or from a registered resource's directory, or the
  kaybee top-level directory

- The site instance, the resource, and its list of parents is available in
  all resource templates
