#!/usr/bin/env python3
"""
Install script for beancount.
"""
__copyright__ = "Copyright (C) 2008-2011, 2013-2016  Martin Blais"
__license__ = "GNU GPLv2"


import os
from os import path
import runpy
import sys
import warnings
import platform


# Check if the version is sufficient.
if sys.version_info[:2] < (3,5):
    raise SystemExit("ERROR: Insufficient Python version; you need v3.5 or higher.")


# Import setup().
setup_extra_kwargs = {}
from setuptools import setup, Extension
has_setuptools = True
setup_extra_kwargs.update(install_requires = [
])

# A note about setuptools: It's profoundly BROKEN.
#
# - The header files are needed in order to distribution a working
#   source distribution.
# - Listing the header files under the extension "sources" fails to
#   build; distutils cannot make out the file type.
# - Listing them as "headers" makes them ignored; extra options to
#   Extension() appear to be ignored silently.
# - Listing them under setup()'s "headers" makes it recognize them, but
#   they do not get included.
# - Listing them with "include_dirs" of the Extension fails as well.
#
# The only way I managed to get this working is by working around and
# including them as "package_data" (see {63fc8d84d30a} below). That
# includes the header files in the sdist, and a source distribution can
# be installed using pip3 (and be built locally). However, the header
# files end up being installed next to the pure Python files in the
# output. This is the sorry situation we're living in, but it works.
#
# If you think I'm a lunatic, fix it and make sure you can make this
# command succeed:
#   nosetests3 -s beancount/scripts/setup_test.py
#

setup(
    name="beancount-financequote",
    version='1.0',
    description="Command-line Double-Entry Accounting",

    long_description=
    """
      A double-entry accounting system that uses text files as input.

      Beancount defines a simple data format or "language" that lets you define
      financial transaction records in a text file, load them in memory and
      generate and export a variety of reports, such as balance sheets or income
      statements. It also provides a client with an SQL-like query language to
      filter and aggregate financial data, and a web interface which renders
      those reports to HTML. Finally, it provides the scaffolding required to
      automate the conversion of external data into one's input file in
      Beancount syntax.
    """,

    license="GNU GPLv2 only",
    author="Martin Blais",
    author_email="blais@furius.ca",
    url="http://furius.ca/beancount",
    download_url="http://bitbucket.org/blais/beancount",

    packages = [
        'beancount_financequote',
    ],

    package_data = {
        'beancount_financequote' : ['financequote.pl'],
        },

    # Add optional arguments that only work with some variants of setup().
    **setup_extra_kwargs
)
