import pytest

pytestmark = pytest.mark.sphinx('html', testroot='typedefs-class')


@pytest.mark.parametrize('page', ['blogpost1.html', ], indirect=True)
class TestInstanceTemplate:
    def test_title(self, page):
        content1 = page.find('h1').contents[0].strip()
        assert content1 == 'Blogpost Typedef from Class'
        content2 = page.find('p').contents[0].strip()
        assert content2 == '999'
