# coding=utf-8
import sys
from setuptools import setup, find_packages

NAME = 'neovim-prompt'
VERSION = '0.1.0'


def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as fi:
        return fi.read()


def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows if x.strip()]
    return list(rows)

setup(
    name=NAME,
    version=VERSION,
    description='A customizable prompt library for Neovim',
    long_description=read('README.rst'),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Text Editors',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    keywords='vim neovim command-line prompt',
    author='Alisue',
    author_email='lambdalisue@hashnote.net',
    url='https://github.com/lambdalisue/%s' % NAME,
    download_url='https://github.com/lambdalisue/%s/tarball/master' % NAME,
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['README.rst',
             'requirements.txt',
             'requirements-test.txt',
             'requirements-docs.txt'],
    },
    zip_safe=True,
    install_requires=readlist('requirements.txt'),
    test_suite='test',
    tests_require=readlist('requirements-test.txt'),
)
