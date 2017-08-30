from kaybee import get_html_templates_path


def test_templates_path():
    r = get_html_templates_path()
    assert r[0].endswith('src/kaybee/resources/article')
    assert r[1].endswith('src/kaybee/templates')
