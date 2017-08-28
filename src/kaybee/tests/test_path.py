from kaybee import convert_path


def test_homepage():
    path = 'index'
    pagename = 'index'
    result = convert_path(path, pagename)
    assert result is 'home'


def test_outside_section():
    path = 'blog/'
    pagename = 'some/where/else'
    result = convert_path(path, pagename)
    assert result is None


def test_section_index():
    path = 'blog/'
    pagename = 'blog/index'
    result = convert_path(path, pagename)
    assert result is 'index'


def test_under_section():
    path = 'blog/'
    pagename = 'blog/some/folder/doc'
    result = convert_path(path, pagename)
    assert result is 'doc'
