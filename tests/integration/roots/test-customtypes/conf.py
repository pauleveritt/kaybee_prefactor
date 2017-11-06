# -*- coding: utf-8 -*-
import os
import sys

import kaybee
from kaybee.core.site_config import SiteConfig

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(here, 'typedefs'))
from article import Article
from section import Section
from genericpage import Genericpage
from hellowidget import HelloWidget
from toctree import Toctree
from category import Category

extensions = [kaybee.__title__]

master_doc = 'index'
html_title = ''
exclude_patterns = ['_build']

kaybee_config = SiteConfig(
    logo=dict(img_url='xyz.png'),
    is_debug=True
)
