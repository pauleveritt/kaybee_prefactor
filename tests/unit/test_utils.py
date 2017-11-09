from kaybee.utils import rst_to_html


def test_rst_to_html():
    source = 'Hello *world*'
    result = rst_to_html(source)
    assert '<div class="document">' in result
    assert '<p>Hello <em>world</em></p>' in result
    assert '</div>' in result
