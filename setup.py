#!/usr/bin/env python

import setuptools
from distutils.core import setup

setup(name='MinerUtils',
      version='2.0.5',
      description='GitHub and Travis API Access Utilities',
      author='Caius Brindescu',
      author_email='caius@brindescu.com',
      url='https://github.com/caiusb/miner-utils',
      packages=['minerutils'],
      install_requires=['requests']
     )
