# import pytest
#
# pytestmark = pytest.mark.sphinx('html', testroot='typedefs-typeinfo')
#
#
# @pytest.mark.parametrize('page', ['typeinfotemplate.html', ], indirect=True)
# class TestTypeinfoTemplate:
#     def test_title(self, page):
#         content = page.find('p').contents[0].strip()
#         assert 'from the typeinfo' in content
