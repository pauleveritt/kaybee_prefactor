========
Features
========

Sphinx has long been used for Python documentation but also for all
kinds of static websites. Kaybee builds on the seriously-awesome machinery
in Sphinx to target two needs:

- Easy to make modern, attractive HTML sites

- Data-driven knowledge bases

Simple Templating
=================

Want certain pages in your site to have a custom template? Instead of
putting massive ``{% if %}`` blocks in your Sphinx ``page.html`` template,
just write a module with this:

.. code-block:: python

    @registry.resource('article')
    class Article(BaseResource):
        pass

Then, save a template named ``article.html`` (by default) in that same
directly. Once you import that module in your Sphinx configuration, you
can put this in any of your Sphinx documents::

  .. article::

...and that document will be rendered with your Jinja2 template.

How did that work? ``@registry.resource('article')`` registered a new
"resource" type with Kaybee, which controls the rendering of Sphinx
documents. Let's look more at this.

Custom Resources
================

In Kaybee, you register classes which create new Sphinx directives,
such as ``.. article::``. When you use that directive in a document, e.g.
at the top, that document becomes a "resource" in Kaybee's resource database.

You can then do lots of things. For example, the Article instance is available
in the template as ``resource``. You can add extra methods and properties
on the class and use it in rendering. Want an uppercase for the title?

.. code-block:: python

    @registry.resource('article')
    class Article(BaseResource):
        @property
        def upper_title(self):
            return self.title.upper()

Now in the ``article.html`` template, you can do:

.. code-block:: jinja

    <h1>Hello {{ resource.upper_title }}</h1>

How does this registry work? It's based on
`Dectate <http://dectate.readthedocs.io>`_, a deeply-useful system for
configuration-driven applications.

YAML Models
===========

Custom resources help us get templates and view logic. But what about
state? Kaybee lets you register a model with a type, then embed resource
state as YAML *inside* a Sphinx document.

Let's say we want a database of authors. Each author is a document in your
Sphinx site. We want to mark those documents as "author" pages. So let's
make a Kaybee resource for author:

.. code-block:: python

    class AuthorModel(BaseResourceModel):
        first_name: str = None
        last_name: str = None


    @registry.resource('author')
    class Author(BaseResource):
        model = AuthorModel

Then, at the top of each author page, e.g. ``paul.rst``, put the following::

    .. author::
        first_name: Paul
        last_name: Everitt

Kaybee makes a new Sphinx directive called ``author``. It then reads the
body of the directive as YAML content and stores the values under the
instance's ``.props`` attribute, then files the instance in the site's
resources database.

The template for this resource type can then do:

.. code-block:: jinja

    <h1>{{ resource.props.first_name }} {{ resource.props.last_name }}</h1>

At this point we have an extensible document database with custom rendering.
Not too bad. But what was up with the ``: str`` variable annotation?

PEP 484 Schemas
===============

Kaybee's models are based on
`pydantic <https://pydantic-docs.helpmanual.io>`_ which does schema
validation based on Python PEP 484 type hinting. Want a value in your YAML
to be required? ``pydantic`` has a solution for that. Want it to be a
certain type? No problem. Default values, nested content, extensible
validation rules, top performance? Ditto.

In the above, if you supplied an integer in the Sphinx document's YAML::

    .. author::
        first_name: 9999999
        last_name: Everitt

...then Kaybee will throw an exception when building the Sphinx docs.

``pydantic`` is fantastic. When combined with a smart editor like PyCharm,
you get type-aware completion and linting, because you're using a standard.

Embeddable Widgets
==================

So far we've talked about resources: marking a document as being an "author".
This lets you make a template that controls the rendering of the page.

What if you want a little block in the middle of page? Kaybee also supports
"widgets" which stick some HTML into the middle of a page. For example,
"hello world":

.. code-block:: python

    from pydantic.main import BaseModel

    from kaybee.registry import registry
    from kaybee.widgets.base import BaseWidget


    class HelloWidgetModel(BaseModel):
        flag: int = 100


    @registry.widget('hellowidget')
    class HelloWidget(BaseWidget):
        model = HelloWidgetModel
        template = 'hellowidget.html'

If your ``conf.py`` imports this module, then you have a new directive
that you can use in the middle of some ReST document::

    Widget Demo
    ===========

    .. hellowidget::
        flag: 99

Your ``hellowidget.html`` Jinja2 template is pretty simple:

.. code-block:: jinja

    <h4>Hello Widget</h4>
    <p id="hellowidget-flag">{{ widget.props.flag }}</p>

This makes it trivial to make, for example, a YouTube video player. But
what if you want to provide listings of your resources?

Query Resources
===============

We now have a database of documents and a way to write custom widgets.
We'd like listings of those resources -- e.g. show me the first 5 tutorials,
marked as published, in reverse date order. Kaybee makes it easy to write
widgets which express queries in YAML, so they can go right in the middle
of a document.

For example, this widget helps a "section" in the site list the resources
it contains:

.. code-block:: python

    class SectionQueryModel(BaseModel):
        template: str
        query: CoreQueryModel


    @registry.widget('sectionquery')
    class SectionQuery(BaseWidget):
        model = SectionQueryModel

        def make_context(self, context, site):
            """ Put information into the context for rendering """

            query = self.props.query
            kbtype = query.kbtype
            sort_value = query.sort_value
            limit = query.limit
            order = query.order
            parent_name = query.parent_name
            q = dict(kbtype=kbtype, sort_value=sort_value, limit=limit,
                     order=order, parent_name=parent_name)
            results = site.filter_resources(**q)
            context['result_count'] = len(results)
            context['results'] = results

You then make a ``sectionquery.html`` template alongside this module. Now
can put this ReST directive inside any document::

    .. sectionquery::

        template: sectionquery.html
        query:
            parent_name: articles/first_series
            rtype: article
            sort_value: title
            order: 1
            limit: 10

References
==========

Any knowledge base wants to have deeply-interlinked content: categories,
topics, tags, authors, etc. For example, a topic of ``django`` might have
15 documents which point at it. You'd like all sides to work well:

- A document that points to ``django`` should have a link to the
  topic page for ``django``

- The ``django`` topic page should list all the documents that point at it
  with links to each

- A "topics" page should list all the known topics, perhaps with a count of
  how many documents are in each topic

Kaybee lets you come up with any kind for references system you want.
For example, make a new reference-style resource called a "category" which
you can use to mark a document as a category::

  .. category::
    label: django

Later, you can goto to a bunch of "article" resources and say they are in
the "django" category::

    .. article::
        published: 2015-01-02 12:01
        weight: 20
        category:
            - python

You can also, in the middle of some text, point at category using normal
Sphinx reference machinery, which fails if the "category" reference type
doesn't exist or "django" doesn't exist as a category::

    :ref:`category-python`
    :ref:`A Link Title <category-python>`

Invalid reference schemes or values are flagged when Sphinx builds the
documents.

In the template, resource classes provide helpers to resolve references, to
make it easy to generate HTML.

Custom Toctrees
===============

Sphinx's table of contents are part of the magic of Sphinx. However,
have a custom presentation of the ordered entries is challenging. Kaybee
makes it easy to replace Sphinx's toctree with your own class and template,
based on the raw data from the underlying toctree.

Extensible Post Renderers
=========================

Kaybee wants you to have full control of the HTML. Some places, such as the
document body, are still under control of Sphinx's HTML builder. These
builders are pluggable, but no fun at all to write.

Kaybee has a "postrenderer" concept where you can register a callable that
is handed the HTML for a rendered page, and returns a transformed string.
Use whatever you want to hack the HTML. For example, an XSLT transform that
converts into a Bootstrap-friendly markup.

Hierarchy Inheritance
=====================

The YAML properties make it really easy to add metadata that can then drive,
for example, styling in sections of the site. But it's a drag to repeat the
same value across tons of documents. It would be great to say, in the
top parent directory, that the "style" is a blue background.

Kaybee supports property inheritance via hierarchies. You can move a property
up to any parent, and then use a special method to get the property from
the lineage.