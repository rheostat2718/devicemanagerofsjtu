#!/bin/python2.6
import IPS
class Package( object ):
    def __init__( self, drvname ):
        self.drvname = drvname
        self.pkg = IPS.package( self.drvname )

        if self.pkg.pkgname:
            self.ispkg = True
        else:
            self.ispkg = False

