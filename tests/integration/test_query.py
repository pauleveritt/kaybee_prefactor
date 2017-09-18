import pytest

pytestmark = pytest.mark.sphinx('html', testroot='queries')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestHomepage:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Test Queries'
