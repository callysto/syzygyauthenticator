#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Juptyer Development Team.
# Distributed under the terms of the Modified BSD License.

#-----------------------------------------------------------------------------
# Minimal Python version sanity check (from IPython/Jupyterhub)
#-----------------------------------------------------------------------------

from __future__ import print_function

import os
import sys

v = sys.version_info
if v[:2] < (3,3):
    error = "ERROR: Jupyter Hub requires Python version 3.3 or above."
    print(error, file=sys.stderr)
    sys.exit(1)


from distutils.core import setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))

# Get the current package version.
version_ns = {}
with open(pjoin(here, 'syzygyauthenticator', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = dict(
    name                = 'syzygyauthenticator',
    packages            = ['syzygyauthenticator'],
    version             = version_ns['__version__'],
    description         = """Override of LocalAuth to handle zfs homedir creation.""",
    author              = "Ian Allison",
    author_email        = "iana@pims.math.ca",
    url                 = "http://jupyter.org",
    license             = "BSD",
    platforms           = "Linux, Mac OS X",
    scripts             = ["zfs-homedir.sh"],
    keywords            = ['Interactive', 'Interpreter', 'Shell', 'Web', 'ZFS'],
    classifiers         = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)

# setuptools requirements
if 'setuptools' in sys.modules:
    setup_args['install_requires'] = install_requires = []
    with open('requirements.txt') as f:
        for line in f.readlines():
            req = line.strip()
            if not req or req.startswith(('-e', '#')):
                continue
            install_requires.append(req)


def main():
    setup(**setup_args)

if __name__ == '__main__':
    main()
