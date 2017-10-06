import pytest

pytestmark = pytest.mark.sphinx('html', testroot='theme-options')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestHomepage:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Test Plain Document'

    def test_logo(self, page):
        img = page.find('img')
        assert 'Kaybee Logo Alt' in img['alt']
        assert 'fake_image.png' in img['src']

    def test_social_media(self, page):
        github = page.find(id='kb-config-github').attrs['href']
        assert github == 'https://github.com/kbtest'
        twitter = page.find(id='kb-config-twitter').attrs['href']
        assert twitter == 'https://twitter.com/kbtest'

    def test_footer(self, page):
        copyright = page.find(id='kb-config-copyright').contents[0].strip()
        assert copyright == '© 2017, All Rights Reserved'
