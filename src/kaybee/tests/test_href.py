from kaybee import convert_href


def test_outside_section():
    href = 'blog/'
    pagename = 'some/where/else'
    result = convert_href(href, pagename)
    assert result is None


def test_section_index():
    href = 'blog/'
    pagename = 'blog/index'
    result = convert_href(href, pagename)
    assert result is 'index'


def test_under_section():
    href = 'blog/'
    pagename = 'blog/some/folder/doc'
    result = convert_href(href, pagename)
    assert result is 'doc'
