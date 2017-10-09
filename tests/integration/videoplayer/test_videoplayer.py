import pytest

pytestmark = pytest.mark.sphinx('html', testroot='videoplayer')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestVideoPlayer:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert 'Test VideoPlayer' == content

    def test_has_widget(self, page):
        player = page.find(class_='kb-videoplayer')
        assert '640' == player.attrs['width']
        assert '360' == player.attrs['height']
        u = 'https://www.youtube.com/embed/yzC2TwhER0c'
        assert u == player.attrs['src']
        assert '0' == player.attrs['frameborder']
