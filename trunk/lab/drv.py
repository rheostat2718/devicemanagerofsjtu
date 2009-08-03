#!/bin/env python

# This script should be run under root priviledge

import os
import sys
uname_i = os.popen( 'uname -i' ).readline()[:-1]
uname_m = os.popen( 'uname -m' ).readline()[:-1]
uname_p = os.popen( 'uname -p' ).readline()[:-1]
#TODO: test uname_p
if uname_p.find( "amd64" ) != -1:
    subdir = 'amd64/'
elif uname_p.find( "sparcv9" ) != -1:
    subdir = 'sparcv9/'
else:
    subdir = ''
USR_KERNEL_DRV = '/usr/kernel/drv'
KERNEL_DRV = '/kernel/drv'
PLATFORM_KERNEL_DRV_I = '/platform/' + uname_i + '/kernel/drv'
PLATFORM_KERNEL_DRV_M = '/platform/' + uname_m + '/kernel/drv'

def findDrvConf( drivername ):
    """
    this function find driver's location by its name,
    and locate its configure file at the same time
    """
    ret = []
    dirlist = [KERNEL_DRV, USR_KERNEL_DRV, PLATFORM_KERNEL_DRV_I]
    if uname_i != uname_m:
        dirlist.append( PLATFORM_KERNEL_DRV_M )
    for currdir in dirlist:
        drvname = currdir + '/' + subdir + drivername
        if os.path.isfile( drvname ):
            # it is said the driver.conf is always in .../drv
            confname = currdir + '/' + drivername + '.conf'
            if os.path.isfile( confname ):
                ret.append( ( drvname, confname ) )
            # TODO: find out whether we should return None or deprecate it
            # else:
            #     ret.append((drvname,None))

    return ret

def findFirstDrvConf( drivername ):
    """
    return first result in the list or None
    """
    try:
        return findDrvConf( drivername )[0]
    except:
        pass

def findDrv( drivername ):
    """
    return driver's path
    """
    ret = []
    for ( a, b ) in findDrvConf( drivername ):
        ret.append( a )
    return ret

def findFirstDrv( drivername ):
    """
    return first driver path
    """
    try:
        ( a, b ) = findDrvConf( drivername )[0]
        return a
    except:
        pass

def loadModule( modname, verbose = True ):
    """
    Remove all old modules before we load new ones,
    try to load all driver
    """
    try:
        unloadModuel( modname, quiet )
    except:
        pass
    if verbose:
        opt = ''
    else:
        opt = ' 2>/dev/null'

    #TODO: should we just load the first one, normally there is only one
    drvlist = findDrv( modname )
    if verbose & drvlist == []:
        print "Module %s not found" % modname
        return

    if verbose:
        print "Module ", modname
    for drv in drvlist:
        if verbose:
            print "Path :", drv
        ret = os.popen( 'modinst ' + drv + opt )
        if ret != 0:
            print "Failed!"

def unloadModule( modname, verbose = True ):
    """
    Try to remove the module we can find
    """
    midlist = findMidByName( modname )
    if midlist == []:
        print 'Module %s not found' % modname
        return

    if verbose:
        print "Module ", modname
    for mid in midlist:
        unloadMid( mid, verbose )

def findIdByName( modname ):
    l = []
    #TODO: decide implementation of findIdByName
    # invoke a C function or `modinfo | grep xxx`
    return l

def unloadMid( idno, verbose = True ):
    if verbose:
        print "Module No :", idno

    ret = os.system( 'modunload -i ' + str( idno ) )
    if verbose:
        if ret != 0:
            print "Failed!"

#FIXME: add_drv & rem_drv automatically do this by
#judge whether / when we need it?
#fopen("/reconfigure","a")
def touchReconf( modname ):
    ret = os.system( 'touch /reconfigure' )
    return ret

#Doc "819-7057"
def Install( drvname, installFromPackage = False ):
#TODO: use pkgadd to install driver automatically
# support "pkgadd"
    os.system( "cp " + drvname + ' ' + USR_KERNEL_DRV + '/' + subdir )
    os.system( "cp " + drvname + '.conf ' + USR_KERNEL_DRV + '/' )
#POSTINSTALL
#TODO: add_drv cannot used on STREAM devices
#Read Doc "816-4855" & reference to man page on
#sad
#autopush
    os.system( "add_drv " + drvname )
#    loadModule(drvname)

def Uninstall( drvname, cleanUpPackage = False ):
#    unloadModule(drvname)
    os.system( "rem_drv -C " + drvname )
#TODO: use pkg??? to uninstall driver do not needd

def PrintModInfo( drvname ):
#TODO: implement PrintModInfo In C & Python
#or invoke modinfo ... you need to be root
    return

#A few test on finddrv
if __name__ == '__main__':
    print findFirstDrvConf( 'sd' ) #/kernel/drv/
    print findFirstDrv( 'pm' )     #/usr/kernel/drv
    print findDrvConf( 'cpc' )     #/platform/i86pc/kernel/drv
    print findDrv( 'nosuchdriver' )
