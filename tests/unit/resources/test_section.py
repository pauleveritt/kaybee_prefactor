from pykwalify.errors import SchemaError
import pytest
from kaybee.resources.section import Section

LOAD = 'kaybee.resources.base_resource.BaseResource.load'
PAGENAME = 'tutorials/index'
RTYPE = 'section'
TITLE = 'These Are Tutorials'


def test_import():
    assert Section.__name__ == 'Section'


def test_construction(monkeypatch):
    monkeypatch.setattr(LOAD, lambda c: dict(style='s1'))
    s = Section(PAGENAME, RTYPE, TITLE, '')
    s.validate(s.props, s.schema)
    assert s.props['style'] == 's1'
    assert s.name == 'tutorials'
    assert s.rtype == 'section'
    assert s.title == TITLE


def test_has_props(monkeypatch):
    content = """
style: is-medium
weight: 90
in_nav: True    
    """
    s = Section(PAGENAME, RTYPE, TITLE, content)
    assert s.props['style'] == 'is-medium'
    assert s.props['weight'] == 90
    assert s.props['in_nav'] is True


def test_is_valid(monkeypatch):
    content = """
style: is-medium
weight: 90
in_nav: True    
    """
    s = Section(PAGENAME, RTYPE, TITLE, content)
    s.validate(s.props, s.schema)


def test_is_invalid(monkeypatch):
    content = """
xstyle: is-medium
    """
    s = Section(PAGENAME, RTYPE, TITLE, content)
    with pytest.raises(SchemaError):
        s.validate(s.props, s.schema)
