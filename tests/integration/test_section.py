import pytest


@pytest.fixture()
def content(app):
    app.build()
    yield app


@pytest.fixture()
def homepage(content):
    yield (content.outdir / 'index.html').text()


@pytest.fixture()
def sectionpage(content):
    yield (content.outdir / 'articles/index.html').text()


# Home page
@pytest.mark.sphinx('html', testroot='sections')
def test_correct_homepage(homepage):
    assert '>Test Sections' in homepage


@pytest.mark.sphinx('html', testroot='sections')
def test_section_appears_in_homepage(homepage):
    assert 'href="/articles">Articles' in homepage


# Section page
@pytest.mark.sphinx('html', testroot='sections')
def test_correct_sectionpage(sectionpage):
    assert '<title>Articles' in sectionpage


@pytest.mark.sphinx('html', testroot='sections')
def test_section_appears_in_section(sectionpage):
    assert '>Article 1' in sectionpage


@pytest.mark.sphinx('html', testroot='sections')
def test_correct_content(sectionpage):
    assert 'Content after YAML.' in sectionpage
