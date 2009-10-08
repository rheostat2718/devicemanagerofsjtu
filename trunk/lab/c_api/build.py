from distutils.core import setup, Extension
setup(name = 'di',version='1.0',ext_modules=[Extension('di',['di.c'])])
setup(name = 'modulec',version='1.0',ext_modules=[Extension('modulec',['modulec.c'])])

