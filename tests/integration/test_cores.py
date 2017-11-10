"""
Test the special singletons, e.g. genericpage, postrenderer

"""

import pytest

pytestmark = pytest.mark.sphinx('html', testroot='customtypes')

ns = dict(atom='http://www.w3.org/2005/Atom')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestHomepage:

    def test_postrenderer(self, page):
        content = page.find(id='postrenderer-flag').contents[0].strip()
        assert '987' == content


@pytest.mark.parametrize('atom_page', ['atom.xml'], indirect=True)
class TestFeed:
    def test_content(self, atom_page):
        assert 'http://some.where' == atom_page.find('./atom:id', ns).text
