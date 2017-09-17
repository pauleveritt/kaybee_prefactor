import pytest


# Home page
@pytest.mark.sphinx('html', testroot='sections')
def test_correct_homepage(app):
    app.build()
    content = (app.outdir / 'index.html').text()
    assert '>Test Sections' in content


@pytest.mark.sphinx('html', testroot='sections')
def test_section_appears_in_homepage(app):
    app.build()
    content = (app.outdir / 'index.html').text()
    assert 'href="/articles">Articles' in content


# Section page
@pytest.mark.sphinx('html', testroot='sections')
def test_correct_sectionpage(app):
    app.build()
    content = (app.outdir / 'articles/index.html').text()
    assert '<title>Articles' in content


@pytest.mark.sphinx('html', testroot='sections')
def test_section_appears_in_section(app):
    app.build()
    content = (app.outdir / 'articles/index.html').text()
    assert '>Article 1' in content


@pytest.mark.sphinx('html', testroot='sections')
def test_correct_content(app):
    app.build()
    content = (app.outdir / 'articles/index.html').text()
    assert 'Content after YAML.' in content
