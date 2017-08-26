'''
To do
- Make fixtures
- Get some coverage
- Rename the config to be more section-focused
- Perhaps have something different for nav
- Get the homepage style/template into config
- Fix sectionpage_template vs. template, use listing/doc in the name
- Figure out "active"
'''


def dummy_sections():
    return [
        dict(path="blog", title="Blog", href="/blog/",
             color='warning'),
        dict(path="articles", title="Blog", href="/blog/",
             sectionpage_template='articlestemplate',
             template='articletemplate',
             color='warning'),
        dict(path="about", title="About", href="/about.html",
             color='success'),
    ]


def test_homepage():
    from kaybee import choose_layout_info
    sections = dummy_sections()
    pagename = 'index'
    li = choose_layout_info(sections, pagename)
    assert li['style'] == 'header-image is-medium'
    assert li['template'] == 'homepage'


def test_homepage_override_template():
    from kaybee import choose_layout_info
    sections = dummy_sections()
    pagename = 'index'
    li = choose_layout_info(sections, pagename, 'customtemplate')
    assert li['style'] == 'header-image is-medium'
    assert li['template'] == 'customtemplate'


def test_listing():
    from kaybee import choose_layout_info
    sections = dummy_sections()
    pagename = 'blog/index'
    li = choose_layout_info(sections, pagename)
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'sectionpage'


def test_listing_sectionoverride_template():
    # config sections override the template for the listing
    from kaybee import choose_layout_info
    sections = dummy_sections()
    pagename = 'articles/index'
    li = choose_layout_info(sections, pagename)
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'articlestemplate'


def test_listing_section_and_doc_override_template():
    # config sections override the template for the listing, but
    # then the doc itself overrides
    from kaybee import choose_layout_info
    sections = dummy_sections()
    pagename = 'articles/index'
    li = choose_layout_info(sections, pagename, 'customtemplate')
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'customtemplate'


def test_listing_docoverride_template():
    from kaybee import choose_layout_info
    sections = dummy_sections()
    pagename = 'blog/index'
    li = choose_layout_info(sections, pagename, 'customtemplate')
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'customtemplate'


def test_leaf_default():
    from kaybee import choose_layout_info
    sections = dummy_sections()
    pagename = 'blog/firstpost'
    li = choose_layout_info(sections, pagename)
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'page'


def test_leaf_override_template():
    from kaybee import choose_layout_info
    sections = dummy_sections()
    pagename = 'blog/firstpost'
    li = choose_layout_info(sections, pagename, 'customtemplate')
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'customtemplate'


def test_leaf_sectionoverride():
    # The sectiondef overrides the template
    from kaybee import choose_layout_info
    sections = dummy_sections()
    pagename = 'articles/firstpost'
    li = choose_layout_info(sections, pagename)
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'articletemplate'


def test_leaf_sectionoverride_docoverrid():
    # The section overrides, then the document leaf overrides
    from kaybee import choose_layout_info
    sections = dummy_sections()
    pagename = 'blog/firstpost'
    li = choose_layout_info(sections, pagename, 'customtemplate')
    assert li['style'] == 'is-bold is-warning'
    assert li['template'] == 'customtemplate'
