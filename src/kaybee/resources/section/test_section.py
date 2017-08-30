import pytest
from kaybee.resources.section import Section

LOAD = 'kaybee.resources.base_resource.BaseResource.load'
PAGENAME = 'articles/index'
RTYPE = 'article'
TITLE = 'These Are Articles'


def test_import():
    assert Section.__name__ == 'Section'


def test_construct(monkeypatch):
    # monkeypatch.setattr(LOAD, lambda c: dict(x=1))
    content = """
style: ''
sort: 90
is_home: true    
    """
    c1 = """

    
    """
    s = Section(PAGENAME, RTYPE, TITLE, c1)
    s.validate(s.props, s.schema)
    assert s.props['x'] == 1


@pytest.mark.skip(reason="no way of currently testing this")
def test_construct2(monkeypatch):
    monkeypatch.setattr(LOAD, lambda c: dict(x=2))
    content = """
style: ''
sort: 90
is_home: True    
    """
    s = Section(PAGENAME, RTYPE, TITLE, content)
    assert s.props['x'] == 2
