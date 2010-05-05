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
