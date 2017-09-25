import pytest

pytestmark = pytest.mark.sphinx('html', testroot='sections')


# @pytest.mark.parametrize('page', ['index.html', ], indirect=True)
# def test_section_appears_in_homepage(page):
#     # page = pages['index.html']
#     content = page.find(href='/articles').contents[0].strip()
#     assert content == 'Articles'
#

# Section page
@pytest.mark.parametrize('page', ['articles/index.html', ], indirect=True)
class TestSectionpage:
    def test_section_appears_in_section(self, page):
        content = page.find(href='article1.html').contents[0]
        assert 'Article 1' == content

    def test_correct_content(self, page):
        section = page.find(id='articles')
        content = section.find('p').contents[0].strip()
        assert content == 'Content after YAML.'
