# -*- coding: utf-8 -*-

import os
import sys

import kaybee

#
# Add the typedefs to pythonpath
from kaybee.core.site_config import SiteConfig

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(here, 'typedefs'))
from blogpost import Blogpost

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
    is_debug=True
)
