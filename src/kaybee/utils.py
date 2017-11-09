"""
Miscellaneous functions used in Kaybee.
"""
from docutils.core import publish_parts


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
