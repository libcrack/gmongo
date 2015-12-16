#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: devnull@libcrack.so
# Date: Wed Jan 28 16:35:57 CET 2015

import os
import re

from setuptools import setup


def read(relpath):
    """
    Return string containing the contents of the file at *relpath* relative to
    this file.
    """
    cwd = os.path.dirname(__file__)
    abspath = os.path.join(cwd, os.path.normpath(relpath))
    with open(abspath) as f:
        return "".join(f.readlines())

NAME = "gmongo"
VERSION = re.search("__version__ = \"(\S+)\"",
                    read("src/__init__.py")).group(1)
DESCRIPTION = "gtk mongo module."
KEYWORDS = "mongo gtk"
AUTHOR = "libcrack"
AUTHOR_EMAIL = "devnull@libcrack.so"
URL = "https://www.github.com/libcrack/gmongo"
LICENSE = read("LICENSE")
PACKAGE_DIR = {NAME: "./src"}
PACKAGES = [NAME]
PACKAGE_DATA = {NAME: ["data/logging.json"]}
INSTALL_REQUIRES = [
    x.replace("-", "_") for x in
    read("requirements.txt").split("\n") if x != ""
]
# TEST_SUITE = "tests"
# TESTS_REQUIRE = ["behave", "mock", "pyparsing", "pytest"]
LONG_DESC = read("README.md") + "\n\n" + read("CHANGES")
PLATFORMS = ["Linux"]
PROVIDES = []

CLASSIFIERS = [
    "Development Status :: 3 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: GPL",
    "Operating System :: OS Independent",
    "Operating System :: POSIX :: Linux",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
]

ENTRY_POINTS = {
    "console_scripts": [
        "gmongo-cli = gmongo.cli.main",
    ],
    "gui_scripts": [
        "gmongo-gtk = gmongo.gui:main",
    ]
}

PARAMS = {
    "platforms": PLATFORMS,
    "name": NAME,
    "version": VERSION,
    "description": DESCRIPTION,
    "keywords": KEYWORDS,
    "long_description": LONG_DESC,
    "author": AUTHOR,
    "author_email": AUTHOR_EMAIL,
    "url": URL,
    "license": LICENSE,
    "packages": PACKAGES,
    "package_dir": PACKAGE_DIR,
    "package_data": PACKAGE_DATA,
    "provides": PROVIDES,
    "requires": INSTALL_REQUIRES,
    "install_requires": INSTALL_REQUIRES,
    # "tests_require":    TESTS_REQUIRE,
    # "test_suite":       TEST_SUITE,
    "classifiers": CLASSIFIERS,
    "entry_points": ENTRY_POINTS,
}

setup(**PARAMS)

# vim:ts=4 sts=4 tw=79 expandtab:
