#!/bin/env python2.6
import di
print dir( di )
print di.DI_BUS_DOWN
print dir( di.Node )
root = di.Node()
print root.get_info()
children = root.get_children()
print len( children )
for child in children:
    print 'N\t', child.get_info()
    proplist = child.get_prop()
    print "property count: ", len( proplist )
    for prop in proplist:
        print 'P\t\t', prop.get_name(), ',', prop.get_type_name(), ',', prop.get_value()
    minorlist = child.get_minor()
    print "minor-node count: ", len( minorlist )
    for minor in minorlist:
        print 'M\t\t', minor.get_info()
