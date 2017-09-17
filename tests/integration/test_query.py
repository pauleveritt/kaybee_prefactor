import pytest


@pytest.mark.sphinx('html', testroot='queries')
def test_title(app):
    app.build()
    content = (app.outdir / 'index.html').text()
    assert '>Test Queries' in content
