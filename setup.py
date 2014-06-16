#!/usr/bin/env python
from setuptools import setup, find_packages
from granicus import __version__

long_description = ''

setup(name='granicus',
      version=__version__,
      packages=find_packages(),
      author='Paul Tagliamonte',
      author_email='paultag@sunlightfoundation.com',
      license='BSD-3',
      url='http://github.com/paultag/python-granicus/',
      description='Experimental Python bindings for the Granicus API',
      long_description=long_description,
      platforms=['any'],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
)
