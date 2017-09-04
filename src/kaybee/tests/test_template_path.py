from kaybee import get_html_templates_path


def test_templates_path():
    r = get_html_templates_path()
    assert r[0].endswith('src/kaybee/templates')
    assert r[1].endswith('src/kaybee/directives/templates')
    assert r[2].endswith('src/kaybee/resources/article')
    assert r[3].endswith('src/kaybee/resources/section')
