#!/bin/env python2.6
import os

"""
This file provides a list of tools.
"""

def reconfigure():
    """
    Tell system to detect hardware changes in the next boot by executing 'touch /reconfigure'.
    You should be root to call it. 
    return value returns whether the call succeeded.
    """
    if os.geteuid() != 0:
        return False
    try:
        fd = os.open( '/reconfigure', os.O_RDONLY | os.O_CREAT )
        os.close( fd )
    except OSError:
        return False
    return True

def localerun( func, localestr = 'en_GB.UTF-8' ):
    """
    LocalesRun sets environment values and restore it after function.
    Currently, it is mainly used to restrict "pkg info" keywords...
"""
    old = os.environ['LC_MESSAGES']
    os.environ['LC_MESSAGES'] = localestr
    value = func()
    os.environ['LC_MESSAGES'] = old
    return value

