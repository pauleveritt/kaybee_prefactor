from ruamel.yaml import load


class Query:
    """ Model stored in the site with the parameters for this query """

    def __init__(self, name, content):
        self.name = name # This should be a unique ID
        self.props = self.load(content)

    @staticmethod
    def load(content):
        """ Provide a way to stub this in tests """

        # If the string of YAML is empty-ish (new lines, etc.)
        # then return an empty dict
        if content.strip() == '':
            return {}
        return load(content)
