from kaybee.widgets import BaseWidget


def test_import():
    assert BaseWidget.__name__ == 'BaseWidget'


def test_construction(base_widget):
    assert base_widget.__class__.__name__ == 'BaseWidget'


def test_instance(base_widget):
    assert base_widget.props['rtype'] == 'section'


def test_name_sorted(base_widget):
    # Do the props one way
    expected = '{"limit": 5, "rtype": "section"}'
    base_widget.props = {'rtype': 'section', 'limit': 5}
    assert base_widget.name == expected
    base_widget.props = {'limit': 5, 'rtype': 'section'}
    assert base_widget.name == expected


def test_template(base_widget):
    assert base_widget.template == 'widget1.html'
