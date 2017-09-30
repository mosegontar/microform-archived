#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup, find_packages

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

required = [
    'requests',
    'requests_cache',
    'tomd',
]

setup(
    name='microform',
    version='0.1.7',
    description='command-line utility for reading articles in the terminal',
    long_description= 'It uses Mercury Web Parser and tomd (an HTML to Markdown converter) to fetch a web page and generate a readable, markdown version of its content. microform serves a purpose similar to other "reader" services, such as Readability, Safari Reader, Firefox Reader View, Instapaper.',
    author='Alexander Gontar',
    author_email='mosegontar@gmail.com',
    url='https://github.com/mosegontar/microform',
    packages=find_packages(exclude=('tests',)),
    #py_modules=['mercury', 'microform'],
    entry_points= {'console_scripts': ['microform = microform:microform:main']},
    install_requires=required,
    include_package_data=True,
    license='MIT',
)
