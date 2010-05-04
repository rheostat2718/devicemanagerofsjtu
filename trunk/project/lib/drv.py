#!/bin/env python

import sys
import traceback

    def dbg_Reload_Module( self ):
        """
            Unload old modules, then reload it
            return value: 0 for succeed, anything else for failed
            Exception: None
        """
        logging.debug( 'reload module' + self.getFullPath() )
        try:
            ret = self.Unload_Module( verbose )
        except:
            ret = -1
        if ret != 0:
            logging.error( 'Cannot unload old module ' + self.drvname )
            return - 1

        try:
            ret = self.Load_Module( verbose )
        except:
            ret = -1
        if ret != 0:
            logging.error( 'Cannot load module ' + self.drvname )
            return - 1

        return 0

    def dbg_Load_Module( self ):
        """
            Load modules
            return value: 0 for succeed, anything else for failed
            Exception: None
        """
        logging.debug( "load module " + self.drvname )
        path = self.getShortPath()
        if not path:
            logging.error( 'Module ' + self.drvname + ' not found' )
            return - 1

        ret = os.system( 'modload -p ' + path )
        return ret

    def dbg_Unload_Module( self ):
        """
            Unload modules
            return value: 0 for succeed, anything else for failed
            Exception: None
        """
        logging.debug( "unload module " + self.drvname )
        try:
            mid = self.getId()
        except:
            mid = None # module not found?
        if mid == None:
            logging.error( 'Module ' + self.drvname + ' not loaded' )
            return - 1

        ret = os.system( 'modunload -i ' + str( mid ) )
        return ret

    def install( self, args ):
        """
            invoke add_drv to install drivers.
            args: 'add_drv' arguments except for driver name
            return value: 0 for succeed, anything else for failed
            Exception: None
        """
        logging.debug( 'install driver ' + self.drvname )
        if self.dev_subpath:
            path = '/usr/kernel/drv/' + self.dev_subpath + '/'
        else:
            path = '/usr/kernel/drv/'

        logging.info( 'Follow these steps:' )
        logging.info( 'copy device driver binary into ' + path )
        logging.info( 'copy device driver configures *.conf into /usr/kernel/drv' )

        #pause()
        ret = os.system( 'add_drv ' + args + ' ' + self.drvname )
        #WARNING: add_drv does not support STREAM devices according to (816-4855.pdf)
        #reference to sad, autopush

        if ret == 0:
            BaseDriver.Touch_Reconfigure()
            logging.info( 'changes may take effect in the next reboot' )
        else:
            logging.error( 'Cannot install module ' + self.drvname )

        return ret

    def uninstall( self ):
        """
            invoke rem_drv to remove drivers.
            return value: 0 for succeed, anything else for failed
            Exception: None
        """
        logging.debug( 'uninstall ' + self.drvname )

        ret = os.system( 'rem_drv ' + self.drvname )

        if ret == 0:
            BaseDriver.Touch_Reconfigure()
            logging.info( 'changes may take effect in the next reboot' )
        else:
            logging.error( 'Cannot remove module ' + self.drvname )

        return ret

class PackageDriver( Driver ):
    def __init__( self, drvname ):
        Driver.__init__( self, drvname )
        if 1:
            import IPS
            self.ispkg = True
            self.pkg = IPS.Package( self.drvname )
            if not self.pkg.pkgname:
                self.ispkg = False

    def install( self ):
        logging.debug( 'install ' + self.pkg.name )
        if not self.pkg.pkgname:
            ret = -1
        else:
            ret = self.pkg.install()
        return ret

    def uninstall( self ):
        logging.debug( 'uninstall ' + self.pkg.name )
        if not self.pkg.pkgname:
            ret = -1
        else:
            ret = self.pkg.uninstall()
        return ret

    def dbg_install_from_file( self, filename ):
        logging.debug( 'install from file ' + filename )
        if not os.path.isfile( filename ):
            ret = -1
        else:
            ret = os.system( 'pkgadd -n ' + filename )
        return ret

    def dbg_uninstall_from_file( self, filename ):
        logging.debug( 'uninstall from file ' + filename )
        if not os.path.isfile( filename ):
            ret = -1
        else:
            ret = os.system( 'pkgrm -n ' + filename )
        return ret

    def info( self ):
        dict = Driver.info( self )
        if self.pkg:
            dict['package'] = self.pkg.info()
        return dict

def usage():
    print "Usage: python drv.py {install | uninstall} drvname"
    print "                        info drvname"

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'install':
            PackageDriver( sys.argv[2] ).install()
        elif sys.argv[1] == 'uninstall':
            PackageDriver( sys.argv[2] ).uninstall()
        elif sys.argv[1] == 'info':
            print PackageDriver( sys.argv[2] ).info()
        else:
            usage()
    except IndexError:
        usage()

"""
Device Driver Manager

Tested methods:
[info] usage: drv.py info sppp

Implementing methods:
[install] drv.py install sppp -v | -q
[uninstall] drv.py uninstall sppp -v | -q
"""
