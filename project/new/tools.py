#!/bin/env python2.6
import os
import logging
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
        logging.debug( 'reconfigure' )
        fd = os.open( '/reconfigure', os.O_WRONLY | os.O_CREAT )
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

def run_devfsadm():
    if os.geteuid() != 0:
        return False
    try:
        logging.debug( 'devfsadm' )
        ret = os.system( "devfsadm -v" )
    except OSError:
        return False
    return ( ret == 0 )

def run_remdrv( drvname, basedir = None ):
    logging.debug( 'rem_drv ' + drvname )
    if basedir:
        opt = " -b " + basedir + ' '
    else:
        opt = ' '
    ret = os.system( 'rem_drv ' + opt + drvname )
    return ret

def run_adddrv( drvname, basedir = None, classname = None, identifyname = None, permission = None, noload = False, policy = None, privilege = None, verbose = True ):
    logging.debug( 'add_drv ' + drvname )
    if basedir:
        opt = " -b " + basedir + ' '
    else:
        opt = ' '
    if classname:
        opt = opt + " -c " + classname + ' '
    if identifyname:
        #seperated by white space
        opt = opt + " -i '" + identifyname + "' "
    if permission:
        opt = opt + " -m '" + permission + "' "
    if noload:
        opt = opt + " -n "
    if policy:
        opt = opt + " -p '" + policy + "' "
    if privilege:
        opt = opt + " -P '" + privilege + "' "
    if verbose:
        opt = opt + " -v "
    ret = os.system( 'add_drv ' + opt + drvname )
    if basedir:
        reconfigure()
    return ret

def run_updatedrv( drvname, basedir = None, change = None, identifyname = None, permission = None, noload = False, policy = None, privilege = None, verbose = True ):
    logging.debug( 'update_drv ' + drvname )
    if basedir:
        opt = " -b " + basedir + ' '
    else:
        opt = ' '
    if noload:
        opt = opt + " -n "
    if verbose:
        opt = opt + " -v "

    if change:
        if change == 'a':
            opt = opt + ' -a '
        elif change == 'd':
            opt = opt + ' -d '
        else:
            return - 1
        if identifyname:
            #seperated by white space
            opt = opt + " -i '" + identifyname + "' "
        if permission:
            opt = opt + " -m '" + permission + "' "
        if policy:
            opt = opt + " -p '" + policy + "' "
        if privilege:
            opt = opt + " -P '" + privilege + "' "

    ret = os.system( 'update_drv ' + opt + drvname )
    if basedir:
        reconfigure()
    return ret
