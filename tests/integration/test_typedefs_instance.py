import pytest

pytestmark = pytest.mark.sphinx('html', testroot='typedefs-instance')


@pytest.mark.parametrize('page', ['instancetemplate.html', ], indirect=True)
class TestInstanceTemplate:
    def test_title(self, page):
        content = page.find('p').contents[0].strip()
        assert 'from the instance' in content
