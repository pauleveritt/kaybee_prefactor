import pytest
from kaybee.site import Site


class DummyResource:
    def __init__(self, name):
        self.name = name


class DummySection:
    rtype = 'section'

    def __init__(self, name, title, weight=0):
        self.name = name
        self.title = title
        self.weight = weight

    def __str__(self):
        return self.name


SAMPLE_SECTIONS = (
    DummySection('8783', 'The First'),
    DummySection('1343', 'Second should sort ahead of first'),
    DummySection('4675', 'Z Last weights first', -10),
    DummySection('9856', 'Z Last No Weight')
)


def test_import():
    assert Site.__name__ == 'Site'


def test_get_succeeds():
    s = Site()
    assert s.get_class('article').__name__ == 'Article'


def test_get_fails():
    s = Site()
    with pytest.raises(KeyError):
        s.get_class('xx')


def test_add_succeeds():
    s = Site()
    s.klasses['dummyresource'] = DummyResource
    dr = DummyResource('someresource')
    s.add(dr)
    assert s[dr.name] == dr


def test_add_bad_class():
    s = Site()
    dr = DummyResource('someresource')
    with pytest.raises(AssertionError):
        s.add(dr)


def test_remove():
    s = Site()
    s.klasses['dummyresource'] = DummyResource
    dr = DummyResource('someresource')
    s.add(dr)
    assert s[dr.name] == dr
    s.remove(dr.name)
    with pytest.raises(KeyError):
        s[dr.name]


def test_sections_empty():
    s = Site()
    assert s._sections is None


def test_simple_cache():
    s = Site()
    s.klasses['dummysection'] = DummySection
    [s.add(i) for i in SAMPLE_SECTIONS]
    sections = s.sections
    assert len(s._sections) == 4


def test_sort():
    s = Site()
    s.klasses['dummysection'] = DummySection
    [s.add(i) for i in SAMPLE_SECTIONS]
    section_ids = [section.name for section in s.sections]
    assert section_ids == [
        SAMPLE_SECTIONS[2].name,
        SAMPLE_SECTIONS[1].name,
        SAMPLE_SECTIONS[0].name,
        SAMPLE_SECTIONS[3].name
    ]
