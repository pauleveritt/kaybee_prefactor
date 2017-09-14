import pytest

pytest_plugins = 'sphinx.testing.fixtures'


@pytest.mark.sphinx('html', testroot='navmenus')
def test_html_entity(app):
    app.build()
    content = (app.outdir / 'index.html').text()
    assert 'Field' in content
