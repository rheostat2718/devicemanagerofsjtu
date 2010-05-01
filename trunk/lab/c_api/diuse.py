#!/bin/env python2.6
import di
print dir( di )
print di.DI_BUS_DOWN
print dir( di.Node )
root = di.Node()
print root.get_info()
children = root.get_child()
print len( children )
for child in children:
    print child.get_info()
    proplist = child.get_prop()
    for prop in proplist:
        print prop.get_name(), prop.get_type()
