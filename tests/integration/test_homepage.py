import pytest


@pytest.mark.sphinx('html', testroot='homepage')
@pytest.fixture()
def content(app):
    app.build()
    homepage = (app.outdir / 'index.html').text()
    yield homepage


@pytest.mark.sphinx('html', testroot='homepage')
def test_title(app, content):
    # app.build()
    # content = (app.outdir / 'index.html').text()
    # assert 'title>Test Homepage' in content
    assert 'title>Test Homepage' in content

#
# @pytest.mark.sphinx('html', testroot='homepage')
# def test_not_in_nav(app):
#     app.build()
#     content = (app.outdir / 'index.html').text()
#     assert content.count('Test Homepage') == 1
#
#
# @pytest.mark.sphinx('html', testroot='homepage')
# def test_has_hero_style(app):
#     app.build()
#     content = (app.outdir / 'index.html').text()
#     assert 'hero-body' in content
#
#
# @pytest.mark.sphinx('html', testroot='homepage')
# def test_not_has_body(app):
#     app.build()
#     content = (app.outdir / 'index.html').text()
#     assert 'Content after YAML' not in content
