import pytest

pytestmark = pytest.mark.sphinx('html', testroot='widgets')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestHomepage:
    """ Articles without properties set """

    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Test Widgets'
