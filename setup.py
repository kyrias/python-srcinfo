import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'srcinfo',
    version = '0.0.8',
    packages = ['srcinfo'],

    description = ('A small library to parse .SRCINFO files'),
    long_description = read('README.rst'),
    url = 'https://github.com/kyrias/python-srcinfo',
    license = 'ISC',

    author = 'Johannes Löthberg',
    author_email = 'johannes@kyriasis.com',

    install_requires = ['parse'],
    tests_require = ['nose'],
    test_suite = 'nose.collector',

    entry_points = {
        'console_scripts': [
            'parse_srcinfo = srcinfo.main:main',
        ]
    },

    keywords = '.SRCINFO makepkg pacman AUR',

    classifiers = [
        "Development Status :: 3 - Alpha",
        'Topic :: System :: Archiving :: Packaging',
        'License :: OSI Approved :: ISC License (ISCL)',
    ],
)
