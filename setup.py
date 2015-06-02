import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'libsrcinfo',
    version = '0.0.0',
    author = 'Johannes Löthberg',
    author_email = 'johannes@kyriasis.com',
    description = ('A small library to parse .SRCINFO files'),
    license = 'ISC',
    keywords = '.SRCINFO makepkg pacman AUR',
    url = 'https://github.com/kyrias/libsrcinfo',
    packages=['libsrcinfo'],
    install_requires=['parse'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        'Topic :: System :: Archiving :: Packaging',
        'License :: OSI Approved :: ISC License (ISCL)',
    ],
)
