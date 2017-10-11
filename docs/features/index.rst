========
Features
========

.. section::
    in_nav: 10
    published: 2017-10-01 00:00
    style: 'is-bold is-info'
    subheading: Brief survey of what Kaybee is good for

Lots of choices out there for generating static sites. What makes Kaybee
different? As an author or a customizer, Kaybee has a number of compelling
features.

Attractive Theme
================

The default theme for Kaybee based on `Bulma <https://bulma.io/>`_ with
an emphasis on mobile responsiveness. Out of the box the theme supports
content organized into nav menus and branded sections with hero blocks
and rich sidebars.

For Sphinx users, the Kaybee theme uses none of the Jinja2 in Sphinx. The
templates are written from scratch for the best user experience. The
JavaScript from Sphinx is curently being re-used, but will likely be
reimplemented.

Rich Content
============

Kaybee inherits Sphinx's rich facilities for organizing content into a
richly-interlinked corpus. Links between documents are automatically
generated and reported as broken if you rename something. Put a marker
within a document and link to that spot: in fact, headings are automatically
link targets.

Kaybee adds even more structure. You can use the hierarchy to push
common properties up into sections, add rich metadata that can be used
as queries, and automate your own custom reference system.

Resources
=========

Put schema-validated metadata into your documents and let Kaybee help
you generate your site structure and templating. Customizers can even
create their own kinds of resources, with custom schemas and templates, as
well as custom logic used in templating.

Widgets
=======

Insert data-driven blocks into your documents by using widgets. Kaybee ships
with several and it is easy to register your own.

References
==========

Want to build a category system? A tag system? Have authors? Each of these
are resources with a simple flag that says they can be a reference. Kaybee
then registers that reference scheme and that reference value, allowing you
to point at them from schemas or inline references.

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

.. toctree::

    theme.rst