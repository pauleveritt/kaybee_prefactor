# -*- coding: utf-8 -*-

import kaybee

extensions = [kaybee.__title__]

master_doc = 'index'
html_theme = 'kaybee'
exclude_patterns = ['_build']

alt = 'Kaybee Logo Alt'
html_context = dict(
    kaybee_config={},
    logo=dict(
        img_url='http://some.site.com/fake_image.png',
        alt=alt
    ),
    social_media=dict(
        twitter='paulweveritt',
        github='pauleveritt'
    )
)

html_additional_pages = {
    'debug': 'debug.json',
}
