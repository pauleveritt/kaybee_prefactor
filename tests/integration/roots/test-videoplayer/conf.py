# -*- coding: utf-8 -*-

import kaybee
from kaybee.core.site_config import SiteConfig

extensions = [kaybee.__title__]

master_doc = 'index'
html_theme = 'kaybee'
exclude_patterns = ['_build']

kaybee_config = SiteConfig(
    logo=dict(
        img_url='http://some.site.com/fake_image.png',
        alt='Kaybee Logo Alt'
    ),
    copyright='2017, All Rights Reserved',
    social_media=dict(
        twitter='kbtest',
        github='kbtest'
    ),
)
