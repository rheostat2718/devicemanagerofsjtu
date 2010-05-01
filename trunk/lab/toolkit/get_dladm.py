#!/bin/python
import os
import sys

cmd = 'dladm show-phys'

def get_dladm():
    text = os.popen( cmd ).readlines()
    """ 
    currently, text is in the following syntax:
    LINK MEDIA STATE SPEED DUPLEX DEVICE
    """
    ret = []
    for line in text[1:]:
        dict = {}
        link, media, state, speed, duplex, device = line.split()[:6]
        dict['LINK'] = link
        dict['MEDIA'] = media
        dict['STATE'] = state
        dict['SPEED'] = speed
        dict['DUPLEX'] = duplex
        dict['DEVICE'] = device
        ret.append( dict )
    return ret

if __name__ == '__main__':
    print get_dladm()
