import pytest
from kaybee.site import Site


class DummyResource:
    rtype = 'resource'

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


SAMPLE_RESOURCES = (
    DummySection('8783', 'The First'),
    DummySection('1343', 'Second should sort ahead of first'),
    DummySection('4675', 'Z Last weights first', -10),
    DummySection('9856', 'Z Last No Weight'),
    DummyResource('4444')
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


def test_section_listing():
    # Filter out non-sections
    pass


def test_nav_menu():
    # Only include things that want to be in the nav menu
    pass


def test_section_sorting():
    s = Site()
    s.klasses['dummysection'] = DummySection
    s.klasses['dummyresource'] = DummyResource
    [s.add(i) for i in SAMPLE_RESOURCES]
    section_ids = [section.name for section in s.sections]
    assert section_ids == [
        SAMPLE_RESOURCES[2].name,
        SAMPLE_RESOURCES[1].name,
        SAMPLE_RESOURCES[0].name,
        SAMPLE_RESOURCES[3].name
    ]
