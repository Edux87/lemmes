#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages

def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version("lemmes/__init__.py")

REQUIREMENTS = [
    'nltk',
    'numpy',
    'scipy',
    'scikit-learn',
    'Cython',
    'simplejson',
    'python-slugify'
]

DESCRIPTION = ("Compact interface for Assisted Machine Learning")
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='Jiazz',
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Edgar Castañeda',
    author_email='edaniel15@gmail.com',
    license='MIT',
    platforms=["linux"],
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    tests_require=['testfixtures'],
    classifiers=[
        'Development Status :: 1.0',
        'Environment :: Console',
        'License :: NonFree',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: NTL :: Lemmas :: Spanish',
    ],
)
