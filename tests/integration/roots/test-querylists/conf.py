# -*- coding: utf-8 -*-

import kaybee

extensions = [kaybee.__title__]
templates_path = ['_templates'] + kaybee.get_html_templates_path()

master_doc = 'index'
html_theme = 'kaybee'
exclude_patterns = ['_build']

alt = 'Kaybee Test Mock'
html_context = dict(
    kaybee_config={},
    logo=dict(
        img_url='http://bulma.io/images/bulma-logo.png',
        alt=alt
    ),
    social_media=dict(
        twitter='paulweveritt',
        github='pauleveritt'
    )
)
