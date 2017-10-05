# -*- coding: utf-8 -*-

import kaybee

extensions = [kaybee.__title__]

master_doc = 'index'
html_theme = 'kaybee'
exclude_patterns = ['_build']

kaybee_config = dict(
    logo=dict(
        img_url='http://some.site.com/fake_image.png',
        alt='Kaybee Logo Alt'
    ),
    social_media=dict(
        twitter='kbtest',
        github='kbtest'
    ),
)
