#!/usr/bin/env python

import codecs
from setuptools import setup

# Version info -- read without importing
_locals = {}
with open('kaybee/_version.py') as fp:
    exec(fp.read(), None, _locals)
version = _locals['__version__']

# README into long description
with codecs.open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='kaybee',
    entry_points={
        'sphinx_themes': [
            'path = kaybee:get_path',
        ]
    },
    version=version,
    description='Sphinx theme based on Bootstrap 4',
    long_description=readme,
    author='Paul Everitt',
    author_email='pauleveritt@me.com',
    url='https://github.com/pauleveritt/kaybee',
    packages=['kaybee'],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
