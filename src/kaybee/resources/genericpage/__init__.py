class Genericpage:
    def __init__(self, docname):
        self.docname = docname

    @classmethod
    def template(cls):
        return cls.__name__.lower() + '.html'
