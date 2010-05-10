#!/bin/env python2.4
import os
import logging

"""
This file provides a list of tools.
"""

def reconfigure( send ):
    """
    Tell system to detect hardware changes in the next boot by executing 'touch /reconfigure'.
    You should be root to call it.
    return value returns whether the call succeeded.
    """
    send( 'reconf' )

def localerun( func, localestr = 'en_GB.UTF-8' ):
    """
    LocalesRun sets environment values and restore it after function.
    Currently, it is mainly used to restrict "pkg info" keywords...
"""
    ret = False
    if os.environ.has_key( 'LC_MESSAGES' ):
        ret = True
        old = os.environ['LC_MESSAGES']
    os.environ['LC_MESSAGES'] = localestr
    value = func()
    if ret:
        os.environ['LC_MESSAGES'] = old
    return value

def run_devfsadm():
    try:
        #logging.debug( 'devfsadm' )
        ret = os.system( "devfsadm -v" )
    except OSError:
        return False
    return ( ret == 0 )

def run_remdrv( send, drvname, basedir = None, removeConfigure = False ):
    #logging.debug( 'rem_drv ' + drvname )
    if basedir:
        opt = " -b " + basedir + ' '
    else:
        opt = ' '
    #original configure file will be removed if use -C
    if removeConfigure:
        opt = opt + ' -C '
    #ret = os.system( 'rem_drv ' + opt + drvname )
    send( 'CMD:rem_drv' + opt + drvname, "Remove Driver" )
    #return ret

def run_adddrv( send, drvname, basedir = None, classname = None, identifyname = None, permission = None, noload = False, policy = None, privilege = None, verbose = True ):
    """
    you may need to copy driver file to drv directory.
    A configure file may be needed.
    """
    #logging.debug( 'add_drv ' + drvname )
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
    #ret = os.system( 'add_drv ' + opt + drvname )
    send( 'CMD:add_drv' + opt + drvname, "Add Driver" )
    if basedir:
        send( 'reconf' )
    #return ret

def run_updatedrv( send, drvname, basedir = None, change = None, identifyname = None, permission = None, noload = False, policy = None, privilege = None, verbose = True ):
    #logging.debug( 'update_drv ' + drvname )
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
            return - 2
        if identifyname:
            #seperated by white space
            opt = opt + " -i '" + identifyname + "' "
        if permission:
            opt = opt + " -m '" + permission + "' "
        if policy:
            opt = opt + " -p '" + policy + "' "
        if privilege:
            opt = opt + " -P '" + privilege + "' "

    send( 'CMD:update_drv' + opt + drvname, "Update Driver" )
    #ret = os.system( 'update_drv ' + opt + drvname )
    if basedir:
        reconfigure( send )
    #return ret

def rebuildIndex( send ):
    # sometimes pkg asks you to rebuild its index, this function just run the script
    if os.geteuid() != 0:
        return False
    ##logging.debug( 'update_drv ' + drvname )
    ret = os.system( 'pkg rebuild-index' )
    return ( ret == 0 )

def pkg_install( send, pkgname, trial = False, visible = '-v' , refresh = True, index = True ):
    if not pkgname:
        return - 2
    #logging.debug( 'pkg install ' + pkgname )
    #possible visible is "-v" "-q" ""
    opt = ' ' + visible + ' '
    if not refresh:
        opt = opt + ' --no-refresh '
    if not index:
        opt = opt + ' --no-index '
    if trial:
        opt = opt + ' -n '
    send( 'CMD:pkg install ' + opt + pkgname, "pkg_install" )

def pkg_uninstall( send, pkgname, trial = False, visible = '-v' , index = True ):
    if not pkgname:
        return - 2
    #logging.debug( 'pkg uninstall ' + pkgname )
    #possible visible is "-v" "-q" ""
    print 1
    opt = ' ' + visible + ' '
    if not index:
        opt = opt + ' --no-index '
    if trial:
        opt = opt + ' -n '
    #ret = os.system( 'pkg uninstall ' + opt + pkgname )
    send( 'CMD:pkg uninstall ' + opt + pkgname , "pkg_uninstall" )
