from unittest.mock import MagicMock

import pytest

from kaybee.widgets.events import process_widget_nodes


@pytest.fixture()
def app(mocker):
    app = MagicMock()

    yield app


@pytest.fixture()
def nodes():
    node1 = MagicMock()
    node1.attributes = dict(
        hidden=0,
        entries=[(None, 'articles/article1')]
    )
    yield [node1, ]


@pytest.fixture()
def doctree(monkeypatch, nodes):
    doctree = MagicMock()
    monkeypatch.setattr(doctree, 'traverse', lambda x: nodes)

    yield doctree


class TestWidgetEvents:
    def test_process_widget_nodes(self, app, doctree, nodes):
        process_widget_nodes(app, doctree, 'fromdocname22')
