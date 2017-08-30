import pytest
from kaybee.events import choose_layout_info


@pytest.fixture
def sections():
    return [
        dict(title='Blog', path='blog/', color='warning'),
        dict(title='Articles', path='articles/',
             listing_template='somelistingtemplate',
             doc_template='somedoctemplate',
             color='warning'),
        dict(title='About', path='about.html', color='success'),
        dict(title='Home', path='index'),
    ]


def test_homepage(sections):
    pagename = 'index'
    li = choose_layout_info(sections, pagename)
    assert li['style'] == 'header-image is-medium'
    assert li['template'] == 'homepage'


def test_homepage_conf_override_template(sections):
    sections[3]['doc_template'] = 'customhome'
    pagename = 'index'
    li = choose_layout_info(sections, pagename)
    assert li['style'] == 'header-image is-medium'
    assert li['template'] == 'customhome'


def test_homepage_override_template(sections):
    pagename = 'index'
    li = choose_layout_info(sections, pagename, 'customtemplate')
    assert li['style'] == 'header-image is-medium'
    assert li['template'] == 'customtemplate'


def test_listing(sections):
    pagename = 'blog/index'
    li = choose_layout_info(sections, pagename)
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'section'


def test_listing_sectionoverride_template(sections):
    # config sections override the template for the listing
    pagename = 'articles/index'
    li = choose_layout_info(sections, pagename)
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'somelistingtemplate'


def test_listing_section_and_doc_override_template(sections):
    # config sections override the template for the listing, but
    # then the doc itself overrides
    pagename = 'articles/index'
    li = choose_layout_info(sections, pagename, 'customtemplate')
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'customtemplate'


def test_listing_docoverride_template(sections):
    pagename = 'blog/index'
    li = choose_layout_info(sections, pagename, 'customtemplate')
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'customtemplate'


def test_leaf_default(sections):
    pagename = 'blog/firstpost'
    li = choose_layout_info(sections, pagename)
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'page'


def test_leaf_override_template(sections):
    pagename = 'blog/firstpost'
    li = choose_layout_info(sections, pagename, 'customtemplate')
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'customtemplate'


def test_leaf_sectionoverride(sections):
    # The sectiondef overrides the template
    pagename = 'articles/firstpost'
    li = choose_layout_info(sections, pagename)
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'somedoctemplate'


def test_leaf_sectionoverride_docoverrid(sections):
    pagename = 'blog/firstpost'
    li = choose_layout_info(sections, pagename, 'customtemplate')
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'customtemplate'


def test_active(sections):
    pagename = 'blog/firstpost'
    li = choose_layout_info(sections, pagename, 'customtemplate')
    assert li['active'] == 'blog'
