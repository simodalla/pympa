#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pympa
version = pympa.__version__

setup(
    name='pympa',
    version=version,
    author='',
    author_email='simodalla@gmail.com',
    packages=[
        'pympa',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.5',
    ],
    zip_safe=False,
    scripts=['pympa/manage.py'],
)
