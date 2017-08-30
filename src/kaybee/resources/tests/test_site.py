import pytest
from kaybee.site import Site


class DummyResource:
    def __init__(self, name):
        self.name = name


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
