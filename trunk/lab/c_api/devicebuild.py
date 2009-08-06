#build from python, anyone want to have a try
from distutils.core import setup, Extension
setup( ext_modules = [Extension( 'device', ['device.c'] )] )
