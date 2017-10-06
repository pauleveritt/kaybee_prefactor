from json import loads

import pytest
from pydantic import ValidationError
from pydantic.main import BaseModel

from kaybee.core.core_type import CoreType


class DummyMissingModel(CoreType):
    pass


class DummyArticleModel(BaseModel):
    in_nav: bool = False
    weight: int = 0


class DummyArticle(CoreType):
    model = DummyArticleModel


class TestCoreType:
    def test_import(self):
        assert CoreType.__name__ == 'CoreType'

    def test_subclass_and_construct(self):
        da = DummyArticle('somepage', 'widget', 'dummyarticle',
                          'Some Page', '')
        assert da.__class__.__name__ == 'DummyArticle'
        assert da.pagename == 'somepage'
        assert da.kind == 'widget'
        assert da.kbtype == 'dummyarticle'
        assert da.title == 'Some Page'
        assert da.props.in_nav is False

    def test_missing_model(self):
        with pytest.raises(AttributeError) as exc:
            DummyMissingModel('somepage', 'widget', 'dummyarticle',
                              'Some Page', '')
        v = "'DummyMissingModel' object has no attribute 'model'"
        assert v == str(exc.value)

    def test_failed_validation(self):
        yaml_content = '''
weight: 'Should Fail'        
        '''
        with pytest.raises(ValidationError) as exc:
            DummyArticle('somepage', 'widget', 'dummyarticle',
                         'Some Page', yaml_content)
        error = loads(exc.value.json())['weight']['error_msg']
        expected = "invalid literal for int() with base 10: 'Should Fail'"
        assert error == expected
