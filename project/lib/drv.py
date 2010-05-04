#!/bin/env python

import sys
import traceback

    def reload( self ):
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

    def load( self ):
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

    def unload( self ):
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
