import pytest

pytestmark = pytest.mark.sphinx('html', testroot='typedefs')


@pytest.mark.parametrize('json_page', ['debug.html', ], indirect=True)
class TestDebugpage:
    def test_title(self, json_page):
        registry = json_page['registry']
        resources = sorted(registry['resources'])
        assert resources == ['article', 'blogpost', 'customsection',
                             'homepage', 'section']

#
# @pytest.mark.parametrize('page', ['instancetemplate.html', ], indirect=True)
# class TestInstanceTemplate:
#     def test_title(self, page):
#         content = page.find('p').contents[0].strip()
#         assert 'from the instance' in content


# @pytest.mark.parametrize('page', ['typeinfotemplate.html', ], indirect=True)
# class TestTypeinfoTemplate:
#     def test_title(self, page):
#         content = page.find('p').contents[0].strip()
#         assert 'from the typeinfo' in content
