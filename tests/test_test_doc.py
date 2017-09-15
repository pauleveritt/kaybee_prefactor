import pytest


@pytest.mark.sphinx('html', testroot='navmenus')
def test_html_entity(app):
    app.build()
    content = (app.outdir / 'index.html').text()
    assert 'Field' in content
