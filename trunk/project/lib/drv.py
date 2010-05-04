class Package( BaseDriver ):
    def __init__( self, drvname ):
        BaseDriver.__init__( self, drvname )
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
