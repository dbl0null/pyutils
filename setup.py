#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import find_packages

setup(
    name='pyutils',
    version='1.2.4',
    description='Utilities for python',
    author='Binh Vu',
    author_email='binhlvu@gmail.com',
    url='https://github.com/binh-vu/pyutils',
    packages=find_packages(exclude=['tests.*', 'tests'])
)
