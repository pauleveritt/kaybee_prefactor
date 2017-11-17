"""
Miscellaneous functions used in Kaybee.
"""
from docutils import nodes
from docutils.core import publish_parts
from docutils.frontend import OptionParser
from docutils.nodes import Node, document, paragraph
from docutils.parsers.rst import Parser
from docutils.utils import new_document


def rst_document(rst_string: str) -> document:
    default_settings = OptionParser(
        components=(Parser,)).get_default_values()
    document = new_document(rst_string, default_settings)
    parser = Parser()
    parser.parse(rst_string, document)
    return document


def rst_to_html(input_string: str) -> str:
    """ Given a string of RST, use docutils to generate html """

    overrides = dict(input_encoding='unicode', doctitle_xform=True,
                     initial_header_level=1)
    parts = publish_parts(
        writer_name='html',
        source=input_string,
        settings_overrides=overrides
    )
    return parts['html_body']


def get_rst_title(rst_doc: Node) -> str:
    """ Given some RST, extract what docutils thinks is the title """

    for title in rst_doc.traverse(nodes.title):
        return title.astext()


def get_rst_excerpt(rst_doc: document, paragraphs: int = 1) -> str:
    """ Given rst, parse and return a portion """

    texts = []
    for count, p in enumerate(rst_doc.traverse(paragraph)):
        texts.append(p.astext())
        if count + 1 == paragraphs:
            break
    return ' '.join(texts)
