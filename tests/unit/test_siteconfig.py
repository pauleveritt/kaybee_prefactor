from kaybee.siteconfig import SiteConfig, Logo


# Not necessary to write tests to cover all the validation. It's
# essentially configuration and can only fail if pydantic fails.

class TestLogo:
    def test_import(self):
        assert Logo.__name__ == 'Logo'

    def test_logo_img_url_no_value(self):
        config_data = dict()
        logo = Logo(**config_data)
        assert logo.img_url is None

    def test_logo_img_url_with_value(self):
        config_data = dict(img_url='iu')
        logo = Logo(**config_data)
        assert logo.img_url == 'iu'


class TestSiteConfig:
    def test_import(self):
        assert SiteConfig.__name__ == 'SiteConfig'

    def test_empty_config(self):
        config_data = dict()
        config = SiteConfig(**config_data)
        assert False is config.is_debug

    def test_logo_img_url(self):
        config_data = dict(is_debug=True)
        config = SiteConfig(**config_data)
        assert True is config.is_debug
