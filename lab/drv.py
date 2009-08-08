#!/bin/env python

# This script should be run under root priviledge

import os
import sys
import module

ModDrvList = module.getModPath().split()
isainfo = os.popen( 'isainfo -k' ).readline()[:-1]
subdir = {'amd64':'amd64/', 'sparcv9':'sparcv9/', 'i386':''}.get( isainfo, '' )

def findDrvConf( drivername ):
    """
    this function find driver's location by its name,
    and locate its configure file at the same time
    """
    ret = []
    for currdir in ModDrvList:
        drvname = currdir + '/' + subdir + drivername
        if os.path.isfile( drvname ):
            # driver.conf is always in .../drv
            confname = currdir + '/' + drivername + '.conf'
            if os.path.isfile( confname ):
                ret.append( ( drvname, confname ) )
            # TODO: find out whether return None or deprecate it
            else:
                ret.append( ( drvname, None ) )

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

#LOADMODULE & UNLOADMODULE are not necessary, but it may be a useful tool in debug?
def loadModule( modname, verbose = True ):
    """
    Remove all old modules before we load new ones,
    try to load all driver
    """
    try:
        unloadModule( modname, verbose )
    except:
        pass
    if verbose:
        opt = ''
    else:
        opt = ' 2>/dev/null'

    #TODO: should we just load the first one, normally there is only one
    drvlist = findDrv( modname )
    if verbose & ( drvlist == [] ):
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
    midlist = findMidByModname( modname )
    if midlist == []:
        print 'Module %s not found' % modname
        return

    if verbose:
        print "Module ", modname
    for mid in midlist:
        unloadMid( mid, verbose )

def findMidByModname( modname ):
    import string
    l = []
    text = os.popen( 'modinfo | grep ' + modname ).readlines()
    for line in text:
        i = line.split( ' ', 1 )[0]
        l.append( string.atoi( i ) )
    return l

def unloadMid( idno, verbose = True ):
    if verbose:
        print "Module No :", idno

    ret = os.system( 'modunload -i ' + str( idno ) )
    if verbose:
        if ret != 0:
            print "Failed!"

def touchReconf( modname ):
    """
    just tell the system to find new hardware in the next boot,
    execute it to setup it manually
    """
    ret = os.system( 'touch /reconfigure' )
    return ret

def installDrv( drvname, installFromPackage = True, verbose = True ):
    """
    Install driver in pkg or use commandline, read document 819-7057
    """
    ( path, filename ) = os.path.split( drvname )
    if installFromPackage:
        import pkg
        pkgname = pkg.findPkg( filename, verbose )
        if pkgname == None:
            print 'No package found'
            return
        else:
            print 'Package ', pkgname, ' found, now installing...'
        ret = pkg.installPackage( pkgname , verbose )
        if ret < 0:
            return
    else:
        """
        install without pkgadd, the driver and its configure file must be in the same directory
        """
        if verbose:
            print ' Copy ', drvname, ' to ', USR_KERNEL_DRV, '/', subdir
        ret = os.system( "cp " + drvname + ' ' + USR_KERNEL_DRV + '/' + subdir )
        if ret != 0:
            print ' Driver ', drvname, ' cannot be installed !'
            return
        if verbose:
            print ' Copy ', drvname, ' to ', USR_KERNEL_DRV, '/'
        ret = os.system( "cp " + drvname + '.conf ' + USR_KERNEL_DRV + '/' )
        if ret != 0:
            print ' Configure file cannot be installed !'
            return
        #TODO: add_drv cannot used on STREAM devices
        #Read Doc "816-4855" & reference to man page on
        #sad
        #autopush
    if verbose:
        print 'Add Module', filename
    ret = os.system( "add_drv " + filename )
    if ret < 0:
        if verbose:
            print ' Add_drv failed!'
        return
    loadModule( filename )
    return 0

def uninstallDrv( drvname, removeFromPackage = True, verbose = True ):
    if verbose:
        print "Unload Module ", drvname
    unloadModule( drvname )
    if verbose:
        print "Remove Module ", drvname
    ret = os.system( "rem_drv -C " + drvname )
    if ret < 0:
        if verbose:
            print 'Operation failed!'
        return
    ( path, filename ) = os.path.split( drvname )
    if removeFromPackage:
        import pkg
        pkgname = pkg.findPkg( filename, verbose )
        if pkgname == None:
            print 'No package found'
            return
        else:
            print 'Package ', pkgname, ' found, now uninstalling...'
        ret = pkg.uninstallPackage( pkgname , verbose )
        if ret < 0:
            return
        else:
            return ret
#    else:
#        os.system( " rm -f drvname" )
#        os.system( ' rm -f ' + drvname + '.conf' )

def PrintModInfo( drvname ):
#TODO: implement PrintModInfo In C & Python
#or invoke modinfo ... you need to be root
    return

def BackupDrvConf():
    return

def RestoreDrvConf():
    return

if __name__ == '__main__':
    if len( sys.argv ) < 2:
        print "Usage: python drv.py [install | uninstall] drvname [-q | -v]"
    else:
        if sys.argv[1] == 'install':
            installDrv( sys.argv[2], True, ( sys.argv[3] == '-v' ) )
        if sys.argv[1] == 'uninstall':
            uninstallDrv( sys.argv[2], True, ( sys.argv[3] == '-v' ) )
