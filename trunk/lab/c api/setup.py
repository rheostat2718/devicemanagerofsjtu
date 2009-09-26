#!/usr/bin/env python

from distutils.core import setup, Extension

MOD='device'
setup(name=MOD, ext_modules=[Extension(MOD, sources=['device.c'])])
