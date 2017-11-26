import dectate
import pytest

from kaybee.plugins.events import EventAction


@pytest.fixture()
def kb():
    class kb(dectate.App):
        event = dectate.directive(EventAction)

    yield kb


@pytest.fixture()
def register_invalid_event(kb):
    @kb.event('xxx', 'somescope')
    def handle_event():
        return

    yield handle_event


@pytest.fixture()
def register_valid_event(kb):
    @kb.event('env-before-read-docs', 'somescope')
    def handle_event():
        return

    yield handle_event


@pytest.fixture()
def query_event(kb, register_valid_event):
    yield dectate.Query('event')


class TestEventAction:
    def test_import(self):
        assert 'EventAction' == EventAction.__name__

    def test_construction(self, kb):
        dectate.commit(kb)
        assert True

    def test_invalid_event_name(self):
        with pytest.raises(AssertionError):
            EventAction('xxx', 'somescope')

    def test_valid_event_name(self):
        ea = EventAction('env-before-read-docs', 'somescope')
        assert 'env-before-read-docs' == ea.name

    def test_get_callbacks(self, kb, register_valid_event):
        dectate.commit(kb)
        callbacks = EventAction.get_callbacks(kb, 'env-before-read-docs')
        assert 1 == len(callbacks)

    def test_get_no_callbacks(self, kb, register_valid_event):
        dectate.commit(kb)
        callbacks = EventAction.get_callbacks(kb, 'xyzpdg')
        assert 0 == len(callbacks)
