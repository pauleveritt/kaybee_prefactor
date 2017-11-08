"""
Test the special singletons, e.g. genericpage, postrenderer

"""

import pytest

pytestmark = pytest.mark.sphinx('html', testroot='customtypes')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestHomepage:

    def test_postrenderer(self, page):
        content = page.find(id='postrenderer-flag').contents[0].strip()
        assert '987' == content