import pytest


@pytest.mark.sphinx('html', testroot='plain-document')
def test_title(app):
    app.build()
    content = (app.outdir / 'index.html').text()
    assert '<title>Test Plain Document' in content


@pytest.mark.sphinx('html', testroot='plain-document')
def test_logo(app):
    app.build()
    content = (app.outdir / 'index.html').text()
    assert 'Kaybee Logo Alt' in content
    assert 'fake_image.png' in content

#
# TODO Need a test that gets the body content inserted, which means
# we need a regular pages to insert content correctly.
#