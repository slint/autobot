#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# This file is part of Autobot.
# Copyright (C) 2015-2019 CERN.
#
# Autobot is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGES.rst') as history_file:
    history = history_file.read()

tests_require = [
    'check-manifest>=0.35',
    'coverage>=4.0',
    'isort>=4.2.15',
    'mock>=1.3.0',
    'pydocstyle>=1.0.0',
    'pytest-cov>=1.8.0',
    'pytest-random-order>=0.5.4',
    "pytest-pep8>=1.0.6",
    'pytest>=3.8.1,<4',
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.6,<1.6',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=2.6.2',
]

install_requires = [
    'github3.py>=0.9.3',
    'click>=7.0',
]

setup(
    author='CERN',
    author_email='info@inveniosoftware.org',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Autobot generates notifications and updates concerning the state of inveniosoftware repositories",
    entry_points={
        'console_scripts': [
            'autobot=autobot.cli:main',
        ],
    },
    install_requires=install_requires,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='autobot',
    name='autobot',
    packages=find_packages(include=['autobot']),
    setup_requires=setup_requires,
    test_suite='tests',
    tests_require=tests_require,
    extras_require=extras_require,
    url='https://github.com/inveniosoftware/autobot',
    version='0.1.0',
    zip_safe=False,
)
