import pytest

pytestmark = pytest.mark.sphinx('html', testroot='plain-document')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestPlainDocument:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Test Plain Document'

    def test_logo(self, page):
        img = page.find('img')
        assert 'Kaybee Logo Alt' in img['alt']
        assert 'fake_image.png' in img['src']

