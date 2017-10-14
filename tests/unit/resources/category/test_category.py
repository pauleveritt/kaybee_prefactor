def test_import(dummy_article):
    assert dummy_article.__class__.__name__ == 'Category'


def test_construction_success(dummy_article):
    assert 'category1' == dummy_article.docname
