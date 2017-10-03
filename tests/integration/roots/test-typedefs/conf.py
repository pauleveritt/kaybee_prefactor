# -*- coding: utf-8 -*-

import os
import sys

import kaybee
#
# Add the typedefs to pythonpath
here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(here, 'typedefs'))
from blogpost import Blogpost

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