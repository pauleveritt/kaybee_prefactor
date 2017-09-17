import pytest


@pytest.fixture()
def content(app):
    app.build()
    yield app


@pytest.fixture()
def homepage(content):
    yield (content.outdir / 'index.html').text()


@pytest.mark.sphinx('html', testroot='queries')
def test_title(homepage):
    assert '>Test Queries' in homepage
