import pytest

pagepaths = ['index.html']


@pytest.mark.sphinx('html', testroot='queries')
def test_title(pages):
    content = pages['index.html'].find('title').contents[0]
    assert content == 'Test Queries'
