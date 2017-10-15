from docutils import nodes


class widget(nodes.General, nodes.Element):
    """ Generic invisible node that goes in doctree.

     When parsing doctrees, we might stumble across, in the middle
     of a document, a widget. The doctree needs a node that can
     be converted to a site.widgets[name] reference. Stick a
     generic, invisible (nothing rendered to output) node in the
     document, then extract (a) the kind of widget (classname) and
     (b) the identifier for the particular widget.

     """

    @property
    def name(self):
        """ This is the identifier for this node """

        return self['ids'][0]

    @property
    def kbtype(self):
        """ The directive used, which finds the class needed

         If our RST has ``.. querylist::``
         """

        n = self.get('names', None)
        if n:
            return n[0]
        return None
