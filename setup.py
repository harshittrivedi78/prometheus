#!/usr/bin/env python

import os
import sys

import info

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def load_requirements(fname):
    with open(fname) as f:
        install_requires = f.read().splitlines()
    return install_requires


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

# packages = ['prometheus']

with open('README.md') as f:
    readme = f.read()
    f.close()

with open('LICENSE') as f:
    LICENSE = f.read()
    f.close()

setup(
    name=info.__name__,
    version=info.__version__,  # get the version of module from __init__ file.
    author=info.__author__,  # get the author of module from __init__ file.
    author_email=info.__author_email__,
    url=info.__url__,
    # packages=packages,  # packages names which is to be installed.

    description='Prometheus client wrapper for django or django rest framework based applications.',
    long_description_content_type='text/markdown',
    long_description=readme,  # put the description after reading from README.txt file.

    # license=LICENSE,
    keywords="prometheus monitoring django django-rest-framework drf client",
    # include_package_data=True,
    options={"bdist_wheel": {"universal": "1"}},
    install_requires=load_requirements("requirements.txt"),

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'Natural Language :: English',
    ],
    python_requires='>=2.7',
)
