import pytest


@pytest.fixture()
def content(app):
    app.build()
    yield app


@pytest.fixture()
def homepage(content):
    yield (content.outdir / 'index.html').text()


@pytest.mark.sphinx('html', testroot='homepage')
def test_title(homepage):
    assert 'title>Test Homepage' in homepage


@pytest.mark.sphinx('html', testroot='homepage')
def test_not_in_nav(homepage):
    assert homepage.count('Test Homepage') == 1


@pytest.mark.sphinx('html', testroot='homepage')
def test_has_hero_style(homepage):
    assert 'hero-body' in homepage


@pytest.mark.sphinx('html', testroot='homepage')
def test_not_has_body(homepage):
    assert 'Content after YAML' not in homepage
