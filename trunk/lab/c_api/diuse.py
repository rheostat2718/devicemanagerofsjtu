#!/bin/env python2.6
import os,sys
ret = os.system("python2.6 build.py build")
if ret != 0:
    sys.exit()
import di
print dir(di)
print dir(di.Node)
n = di.Node()
print n.get_info()
l = n.get_child()
print len(l)
for i in range(len(l)):
    print l[i].get_info()