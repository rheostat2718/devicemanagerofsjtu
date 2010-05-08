#!/bin/python

import os
#import tools

cols = 'ap_id:class:type:r_state:o_state:condition:busy:physid:status_time_p:info'
#ap_id, device class, device type, Receptacle, Occupant

if __name__ == '__main__':

    output = os.popen( 'cfgadm -a -s cols=' + cols ).readlines()
    list = []
    for line in output:
        list.append( line.split( None, 9 ) )
    for line in list:
        print line, len( line )
