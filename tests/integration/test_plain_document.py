import pytest

pagepaths = ['index.html']


@pytest.mark.sphinx('html', testroot='plain-document')
def test_titles(pages):
    page = pages['index.html']
    content = page.find('title').contents[0]
    assert content == 'Test Plain Document'


@pytest.mark.sphinx('html', testroot='plain-document')
def test_logo(pages):
    page = pages['index.html']
    img = page.find('img')
    assert 'Kaybee Logo Alt' in img['alt']
    assert 'fake_image.png' in img['src']

#
# TODO Need a test that gets the body content inserted, which means
# we need a regular pages to insert content correctly.
#