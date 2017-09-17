import pytest


@pytest.fixture()
def content(app):
    app.build()
    yield app


@pytest.fixture()
def plainpage(content):
    yield (content.outdir / 'index.html').text()


@pytest.mark.sphinx('html', testroot='plain-document')
def test_title(plainpage):
    assert '<title>Test Plain Document' in plainpage


@pytest.mark.sphinx('html', testroot='plain-document')
def test_logo(plainpage):
    assert 'Kaybee Logo Alt' in plainpage
    assert 'fake_image.png' in plainpage

#
# TODO Need a test that gets the body content inserted, which means
# we need a regular pages to insert content correctly.
#