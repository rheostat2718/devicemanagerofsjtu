#!/bin/env python2.6
import os
import sys
from c_api.modulec import *
import package
class Driver():
    def __init__( self, drvname ):
        self.drvname = drvname
        try:
            self.defaultdrvpath, self.defaultconfpath = getFirstDriverPathConf()
        except:
            self.defaultdrvpath = ''
            self.defaultconfpath = ''
        self.updateInfo()
    def dbg_setDefaultDrvPath( self, path ):
        self.defaultdrvpath = path
    def dbg_setDefaultConfPath( self, path ):
        self.defaultconfpath = path
    def updateInfo( self ):
        info = self.getInfo()
        self.isdrv = ( info['INSTALLED'] != 0 )
        self.isload = ( info['LOADED'] != 0 )

    def getAllDriverPath( self ):
        ret = []
        for ( a, b ) in findDrvConf( self.drvname ):
            ret.append( a )
        return ret

    def getFirstDriverConfPath( self ):
        return self.getAllDriverConfPath()[0]

    def getFirstDriverPath( self ):
        return self.getAllDriverPath()[0]

    def getAllDriverConfPath( self ):
        """
        This function finds driver's locations, and also locate driver.conf at the same time
        """
        import module
        #Having more than 2 subdir is completely possible, e.g. some on 32b system and others on 64b system
        subdirlist = []
        mapdict = {'amd64':'amd64', 'sparcv9':'sparcv9', 'i386':'.'}
        for name in os.popen( 'isainfo -k' ).readline().split():
            subdirlist.append( mapdict[name] )
        ret = []
        for currdir in getModPath().split:
            for subdir in subdirlist:
                drvname = currdir + os.path.sep + 'drv' + os.path.sep + subdir + os.path.sep + self.drvname
                if os.path.isfile( drvname ):
                    # driver.conf is always in something..../drv
                    confname = currdir + os.path.sep + 'drv' + os.path.sep + self.drvname + '.conf'
                    if os.path.isfile( confname ):
                        ret.append( ( drvname, confname ) )
#FIXME: I don't know whether should return None or deprecate it
                    else:
                        ret.append( ( drvname, None ) )
        return ret

    def dbg_loadModule( self, verbose = True ):
        """
        First try to remove old modules before we proceed, then we load it
        """
        self.updateInfo()
        if not self.isdrv:
            if verbose:
                print "Module %s not found" % self.drvname
            return
        if self.isload:
            try:
                ret = self.dbg_unloadModule( verbose )
            except:
                if verbose:
                    print 'Cannot unload old module : ', self.drvname
        self.updateinfo()
        if  self.isload:
            if verbose:
                print 'Cannot unload old module : ', self.drvname
                return
        if verbose:
            print "Module ", self.drvname, ':', self.defaultdrvpath, ':'
            opt = ''
        else:
            opt = ' 2>/dev/null'

        ret = os.popen( 'modinst ' + self.defaultdrvpath + opt )
        if verbose:
            if ret != 0:
                print 'Failed'
            else:
                print 'Succeed'
        self.updateInfo()
        return ret

    def dbg_unloadModule( self, verbose = True ):
        self.updateInfo()
        if not self.isdrv:
            if verbose:
                print "Module %s not found" % self.drvname
            return
        if not self.isload:
            print 'Module %s not loaded' % self.drvname
            return
        else:
            idno = self.getId()
        if idno == None:
            print 'Module %s not loaded' % self.drvname
            return
        if verbose:
            print "Module :", self.drvname, ': Id', idno
        ret = os.system( 'modunload -i ' + str( idno ) )
        if verbose:
            if ret != 0:
                print 'Failed'
            else:
                print 'Succeed'
        self.updateInfo()
        return ret

    def dbg_touchReconf():
        """
        just tell the system to find new hardware in the next boot,
        execute it to setup it manually
        """
        return os.system( 'touch /reconfigure' )

    def Backup( self ):
        return
    def Restore( self ):
        return
    def isBackup( self ):
        return False

    def getInfo( self ):
        id = self.getId()
        if id == None:
            return
        try:
            return getModuleInfo( id )
        except:
            pass

    def getId( self ):
        try:
            return getModuleId( self.drvname )
        except:
            return None

    def Install( self, verbose = True, InstallFromPackage = True, arg = None ):
        try:
            if InstallFromPackage:
                Install_Pkg( verbose, arg )
            else:
                Install_Cpy( verbose, arg )
        except:
            pass

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

if __name__ == '__main__':
    if len( sys.argv ) < 2:
        print "Usage: python drv.py [install | uninstall | info] drvname [-q | -v]"
    else:
        if sys.argv[1] == 'install':
            installDrv( sys.argv[2], True, ( sys.argv[3] == '-v' ) )
        if sys.argv[1] == 'uninstall':
            uninstallDrv( sys.argv[2], True, ( sys.argv[3] == '-v' ) )
        if sys.argv[1] == 'info':
            print( Driver( sys.argv[2] ).getInfo() )
