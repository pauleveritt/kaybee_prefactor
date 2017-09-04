import pytest
from kaybee.site import Site


class DummyResource:
    rtype = 'resource'

    def __init__(self, name, title, in_nav=False, weight=0):
        self.name = name
        self.title = title
        self.props = dict(
            in_nav=in_nav,
            weight=weight
        )


class DummySection:
    rtype = 'section'

    def __init__(self, name, title,
                 in_nav=False, weight=0):
        self.name = name
        self.title = title
        self.props = dict(
            in_nav=in_nav,
            weight=weight
        )

    def __str__(self):
        return self.name


SAMPLE_RESOURCES = (
    DummySection('8783', 'The First', in_nav=True),
    DummySection('1343', 'Second should sort ahead of first'),
    DummySection('4675', 'Z Last weights first', in_nav=True),
    DummySection('9856', 'Q Not Last No Weight', in_nav=True),
    DummyResource('4444', 'About', in_nav=True)
)


def test_import():
    assert Site.__name__ == 'Site'


def test_get_succeeds():
    s = Site(dict())
    assert s.get_class('article').__name__ == 'Article'


def test_get_fails():
    s = Site(dict())
    with pytest.raises(KeyError):
        s.get_class('xx')


def test_add_succeeds():
    s = Site(dict())
    s.klasses['dummyresource'] = DummyResource
    dr = DummyResource('someresource', 'Some Resource')
    s.add(dr)
    assert s[dr.name] == dr


def test_add_bad_class():
    s = Site(dict())
    dr = DummyResource('someresource', 'Some Resource')
    with pytest.raises(AssertionError):
        s.add(dr)


def test_remove():
    s = Site(dict())
    s.klasses['dummyresource'] = DummyResource
    dr = DummyResource('someresource', 'Some Resource')
    s.add(dr)
    assert s[dr.name] == dr
    s.remove(dr.name)
    with pytest.raises(KeyError):
        s[dr.name]


def test_section_listing():
    # Filter out non-sections
    s = Site(dict())
    s.klasses['dummysection'] = DummySection
    s.klasses['dummyresource'] = DummyResource
    [s.add(i) for i in SAMPLE_RESOURCES]

    assert len(s.sections) == len(SAMPLE_RESOURCES) - 1


def test_all_resources():
    # Filter out non-sections
    s = Site(dict())
    s.klasses['dummysection'] = DummySection
    s.klasses['dummyresource'] = DummyResource
    [s.add(i) for i in SAMPLE_RESOURCES]

    assert len(s.all_resources) == len(SAMPLE_RESOURCES)


SAMPLE_RESOURCES2 = (
    DummySection('8783', 'The First', in_nav=True),
    DummySection('1343', 'Second should sort ahead of first'),
    DummySection('4675', 'Z Last weights first', in_nav=True),
    DummySection('9856', 'Q Not Last No Weight', in_nav=True, weight=-10),
    DummyResource('4444', 'About', in_nav=True, weight=20)
)


def test_nav_menu():
    # Only include things that want to be in the nav menu,
    # sorted by weight then by title

    s = Site(dict())
    s.klasses['dummysection'] = DummySection
    s.klasses['dummyresource'] = DummyResource
    [s.add(i) for i in SAMPLE_RESOURCES2]
    navmenu_ids = [navmenu.name for navmenu in s.navmenu]
    assert navmenu_ids[0] == SAMPLE_RESOURCES2[3].name
    assert navmenu_ids[1] == SAMPLE_RESOURCES2[0].name
    assert navmenu_ids[2] == SAMPLE_RESOURCES2[2].name
    assert navmenu_ids[3] == SAMPLE_RESOURCES2[4].name
