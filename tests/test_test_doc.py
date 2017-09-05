import pytest
import re

pytest_plugins = 'sphinx.testing.fixtures'


@pytest.mark.sphinx('html', testroot='navmenus')
def test_html_entity(app):
    app.builder.build_all()
    valid_entities = {'amp', 'lt', 'gt', 'quot', 'apos'}
    content = (app.outdir / 'index.html').text()
    for entity in re.findall(r'&([a-z]+);', content, re.M):
        assert entity not in valid_entities
