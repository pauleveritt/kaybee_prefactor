import pytest
from pydantic import ValidationError

from kaybee.resources import BaseResource
from kaybee.resources.article import Article
from kaybee.resources.homepage import Homepage
from kaybee.resources.section import Section


class Site:
    def __init__(self):
        self.resources = {}

    def get_reference(self, kbtype, label):
        pass


@pytest.fixture
def site():
    f1_content = """
template: f1_section_template.html
overrides:
    article:
        template: override_article.html
    section:
        style: f1style    
    """
    index = Homepage('index', 'homepage', '')
    about = Article('about', 'article', '')
    f1 = Section('f1/index', 'section', f1_content)
    f1_about = Article('f1/about', 'article', '')
    f2 = Section('f1/f2/index', 'section', '')
    f2_about = Article('f1/f2/about', 'article', '')
    f3 = Section('f1/f2/f3/index', 'section', 'style: f3style')
    f3_about = Article('f1/f2/f3/about', 'article', '')
    f4 = Section('f1/f2/f3/f4/index', 'section', '')
    s = Site()
    s.resources = {
        'index': index,
        'about': about,
        'f1/index': f1,
        'f1/about': f1_about,
        'f1/f2/index': f2,
        'f1/f2/about': f2_about,
        'f1/f2/f3/index': f3,
        'f1/f2/f3/about': f3_about,
        'f1/f2/f3/f4/index': f4
    }
    yield s


def test_import():
    assert BaseResource.__name__ == 'BaseResource'


def test_instance():
    da = Article('somepage', 'article', '')
    assert da.__class__.__name__ == 'Article'
    assert da.docname == 'somepage'
    assert da.name == 'somepage'
    assert da.parent == 'index'
    assert da.kbtype == 'article'
    assert da.props.in_nav is False


@pytest.mark.parametrize('docname, parents_len, parentname', [
    ('index', 0, 'site'),
    ('about', 1, 'index'),
    ('f1/index', 1, 'index'),
    ('f1/about', 2, 'f1/index'),
    ('f1/f2/index', 2, 'f1/index'),
    ('f1/f2/about', 3, 'f1/f2/index'),
    ('f1/f2/f3/index', 3, 'f1/f2/index'),
    ('f1/f2/f3/about', 4, 'f1/f2/f3/index'),
])
def test_root_parents(site, docname, parents_len, parentname):
    a = site.resources[docname]
    parents = a.parents(site)
    assert parents_len == len(parents)
    if parents_len:
        assert 'index' == parents[-1].docname  # Homepage
        assert parentname == parents[0].name


class TestFindProp:
    def test_find_prop_none_local(self, site):
        a = Article('f1/f2/f3/f4/about', 'kbtype', '')
        prop = a.find_prop(site, 'foo')
        assert None is prop

    def test_section_nonesite(self, site):
        a = Article('xxx1/xxx2/xxx3/about', 'kbtype', '')
        assert None is a.section(site)


def test_section_f1(site):
    a = Article('f1/f2/f3/another', 'kbtype', '')
    assert 'f1/f2/f3/index' == a.section(site).docname


@pytest.mark.parametrize('docname, nav_href, expected', [
    ('f1/index', 'f1/index', True),
    ('f1/index', 'f2/index', False),
    ('f2/index', 'f1/index', False),
    ('f1/about', 'f1/index', True),
    ('f1/about', 'f2/index', False),
    ('f1/f2/index', 'f1/index', True),
    ('f1/f2/about', 'f2/index', False),
])
def test_is_active(site, docname, nav_href, expected):
    a = Article(docname, 'kbtype', '')
    assert a.is_active_section(site, nav_href) == expected


@pytest.fixture()
def da(site):
    yield site.resources['f1/f2/f3/about']


class TestInheritedProperty:

    def test_template_from_props(self, site, da):
        expected = 'f1_section_template.html'
        assert expected == site.resources['f1/index'].template(site)

    def test_template_from_section(self, site, da):
        expected = 'override_article.html'
        assert expected == da.template(site)

    def test_template_from_class(self, site, da):
        # Delete the lineage-inheried article template prop on the section
        f1 = site.resources['f1/index']
        del f1.props.overrides['article']
        assert 'article.html' == da.template(site)

    def test_style_from_props(self, site):
        da = site.resources['f1/f2/f3/index']
        assert 'f3style' == da.style(site)

    def test_style_from_section(self, site):
        da = site.resources['f1/f2/index']
        assert 'f1style' == da.style(site)

    def test_style_from_class(self, site):
        # Delete the lineage-inherited article template prop on the section
        del site.resources['f1/index'].props.overrides['section']
        da = site.resources['f1/f2/index']
        assert 'section.html' == da.style(site)


@pytest.mark.parametrize('content, expected', [
    ('', False),
    ('published: 2020-12-01 01:23', False),
    ('published: 2012-03-24 11:47', True),
])
def test_is_published(content, expected):
    article = Article('d1/a1', 'article', content)
    assert expected is article.is_published()


class TestReferences:
    def test_empty(self):
        content = ''
        article = Article('d1/a1', 'article', content)
        assert [] == article.props.tag

    def test_reference_fieldnames(self):
        article = Article('d1/a1', 'article', '')
        field_names = article.reference_fieldnames
        assert ['category', 'tag'] == field_names

    def test_valid(self):
        content = """
tag:
    - tag1
    - tag2
    - tag3        
        """
        article = Article('d1/a1', 'article', content)
        assert ['tag1', 'tag2', 'tag3'] == article.props.tag

    def test_invalid(self):
        content = """
tag:
    - tag1
    - tag2
    - 9999999        
        """
        with pytest.raises(ValidationError):
            Article('d1/a1', 'article', content)

    def test_helper_valid(self):
        content = """
tag:
    - tag1
    - tag2
    - tag3        
        """
        article = Article('d1/a1', 'article', content)
        assert ['tag1', 'tag2', 'tag3'] == article.props.tag

    def test_references(self, monkeypatch, site):
        content = """
        tag:
            - tag1
            - tag2
            - tag3        
                """

        # Monkeypatch the site to have some tags already registered
        article = Article('d1/a1', 'article', content)
        site_references = dict(
            tag=dict(
                tag1=101,
                tag2=202,
                tag3=303
            )
        )
        gr = lambda fn, label: site_references[fn][label]
        monkeypatch.setattr(site, 'get_reference', gr)

        references = article.references(site)
        assert [101, 202, 303] == references['tag']
