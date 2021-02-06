#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()

setup(
    name='experpy',
    version='1.753.10',
    license='Apache 2.0',
    description='An example package. Generated with cookiecutter-pylibrary.',
    author='Ben Davidson',
    author_email='ben.davidson6@googlemail.com',
    packages=['experpy'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'gitpython',
    ],
    setup_requires=[
        'pytest-runner',
    ]
)