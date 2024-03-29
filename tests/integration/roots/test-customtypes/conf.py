# -*- coding: utf-8 -*-
import os
import sys

import kaybee
from kaybee.siteconfig import SiteConfig

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(here, 'typedefs'))
import article, category, genericpage, hellowidget, section, toctree, \
    postrenderer

extensions = [kaybee.__title__]

master_doc = 'index'
html_title = ''
exclude_patterns = ['_build']

kaybee_config = SiteConfig(
    logo=dict(img_url='xyz.png'),
    feed_url='http://some.where',
    is_debug=True
)
