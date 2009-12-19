#!/bin/python

import os

os.chdir('./lib')
os.system("gksu -m you\ should\ have\ to\ be\ root python __init__.py")
