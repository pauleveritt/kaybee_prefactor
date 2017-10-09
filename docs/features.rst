========
Features
========

.. article::

Templating
==========

- A resource can specify a template in YAML, inherit it from the section,
  or fall back on getting it from the class name.

- The template file named can be come from the ``_templates`` directory
  in the conf directory, or from a registered resource's directory, or the
  kaybee top-level directory

- The site instance, the resource, and its list of parents is available in
  all resource templates

Layout and Styling
==================

- Completely new HTML templating, nothing shared from Sphinx

- Focused on modern-looking and acting sites, responsive, with CSS from
  a decent project (currrently Bulma and SCSS) and decent JS support, both
  using Webpack with a focus on small bundle sizes

- Also focused on using tools, so dropped the ``css_t`` approach from Sphinx

- Re-implement the majority of Sphinx basic styling

- kaybee theme has a section style and resources can get style from YAML,
  lineage, then class

- Conventional set of Jinja2 slots that can be filled

- The layout has a hero section that can be filled by a resource/section's
  template. The homepage template fills with a taller, richer hero display.

- Move document_settings <script> to its own template to avoid screwing


Nav Menus
=========

- Put a resource into the nav menu

- Active nav menu

- Weights adjust sort order

Resources
=========

- Embed YAML in RST to turn a document into a resource with properties
  enforced by a schema

- Schemas default to a same-named YAML file next to the resource class,
  but can be overridden by the class

- Ditto for the template name

- Lineage properties for style, template, etc.

- Remove some noise from the generated RST->HTML e.g. extra heading

- kaybee stamps the resource type named in the decorator, onto the
  resource class (to avoid duplication)

- Intelligent handling of page names, treating folder/index as folder
  being the actual resource

- Determine which section the resource is in

Widgets
=======

- Logic and layout in the middle of a page, driven by a directive

- Easily write new widgets with new property schemas, logic, and templates

References
==========

- Resources can be marked as a reference value by having a "label"
  property that returns a shorthand reference marker

- Other resources can point to that resource, e.g. a certain category,
  via that label as a value on a schema field that is flagged as a reference

- Reference values are then enforced during building

- You can also use a Sphinx reference with this special scheme, e.g.::

    :ref:`category-python`
    :ref:`A Link Title <category-python>`

Site
====

- Maintain a mapping of resources and widgets

- List the sections

- Perform queries: filter on resource type, sort attribute, sort order,
  limit

- Configure site with schema-validated YAML

Extending
=========

- Write new resources and widgets outside of kaybee and register with the
  configuration system

- Both are easier to write than normal Sphinx

Miscellaneous
=============

- Configuration-driven system based on Dectate

- Extensive unit and integration tests

- Video player widget
