#!/bin/python2.6
import os
import sys
import logging

#import logger
from pkglist import *
import tools

class Package( object ):
    """
    This class execute "pkg install | uninstall | list | info | search,
    provides an interface to PackageDrv
    
    __init__(self,name):
    select(self,list):
    validate(self,pkgname):
    search(self):
    get_pkglist(self):
    GetNameList(self,lines,filter=None):
    GetFMRI(self,lines,filter=None):
    GetLatestVersion(self,lines,filter=None):
    try_install(self):
    try_uninstall(self):
    info(self):
    install( self ):
    uninstall( self ):
    getShortName(self,name):
    """
    def __init__( self, drvname, pkgname = None ):
        self.name = drvname

        if pkgname:
            if self.validate( pkgname ):
                self.pkgname = pkgname
                combineDict( {self.name:self.pkgname} )
            else:
                pkgname = None

        if not pkgname:
            self.pkgname = self.search()
            #print self.pkgname

    def GetFMRI( self, lines, filter = None ):
        pkg = []
        for line in lines:
            line = line[:-1]
            #print line
            try:
                index, action, value, package = line.split()
                if ( action != 'file' ) | ( not index ) | ( not package ):
                    continue
                if filter and ( index != filter ):
                    continue
                if value.find( '/drv' ) == -1:
                    continue #make sure it is a driver
                if not ( package in pkg ):
                    pkg.append( package )
            except ValueError:
                continue
        return pkg

    def GetLatestVersion( self, lines, filter = None ):
        pkg = {}
        for line in lines:
            line = line[:-1]
            #print line
            try:
                index, action, value, package = line.split()
                if ( action != 'file' ) | ( not index ) | ( not package ):
                    continue
                if filter and ( index != filter ):
                    continue
                if value.find( '/drv' ) == -1:
                    continue #make sure it is a driver
                ( prefix, version ) = package.split( '@', 1 )

                if not ( prefix in pkg ):
                    pkg[prefix] = version
                elif self.dbg_compareFMRI( version, pkg[prefix] ) > 0:
                    pkg[prefix] = version
            except ValueError:
                continue

        pkglist = []
        for prefix in pkg.keys():
            pkglist.append( prefix + '@' + pkg[prefix] )
        logging.info( str( len( pkglist ) ) + ' matches:' )
        return pkglist

    def try_install( self, send ):
        return tools.pkg_install( send, self.pkgname, trial = True )

    def try_uninstall( self, send ):
        return tools.pkg_uninstall( send, self.pkgname, trial = True )

    def get_pkglist( self ):
        """
        execute "pkg search -lr <name>" to get package name list
        """
        text = os.popen( 'pkg search -lr ' + self.name ).readlines()
        list = self.GetNameList( text )
        if list:
            pkg = self.select( list )
            combineDict( {self.name:pkg} )
            dumpDict()
        else:
            pkg = None
        return pkg

    def GetNameList( self, lines, filter = None ):
        """
        input: "pkg search ..." output
        output: pkgnamelist
        """
        pkg = []
        for line in lines:
            line = line[:-1]
            logging.info( line )
            try:
                llist = line.split()
                package = llist[-1]
                value = llist[-2]
                index, action, value, package = line.split()
                if ( action != 'file' ) | ( not index ) | ( not package ):
                    continue
                if filter and ( index != filter ):
                    continue
                if value.find( '/drv' ) == -1:
                    continue #make sure it is a driver
                ( prefix, version ) = package.split( '@', 1 )
                ( type, name ) = prefix.split( ':/', 1 )
                if not ( name in pkg ):
                    pkg.append( name )
                #pkg install always install the latest package when provided with name

            except ValueError:
                continue

        return pkg

    def select( self, list ):
        #by default, choose the first, and it's always the only one
        if list:
            return list[0]

    def validate( self, pkgname ):
        logging.debug( "validate " + pkgname )
        lines = os.popen( 'pkg contents -t file ' + pkgname + '| grep "kernel\/drv"' )
        for line in lines:
            filename = line[:-1].split( '/' )[-1]
            if filename == self.name:
                logging.info( "find item " + line[:-1] )
                return True
        logging.info( self.name + " not found in " + pkgname )
        return False

    def search( self ):
        pkgdict = fastload()
        if pkgdict.has_key( self.name ):
            return pkgdict[self.name]
        pkgname = self.get_pkglist()
        return pkgname

    def install( self , send ):
        return tools.pkg_install( send, self.pkgname )

    def uninstall( self, send ):
        return tools.pkg_uninstall( send, self.pkgname )

    def getShortName( self, name ):
        list = name.split( '@' )
        if len( list ) == 1:
            return name
        else:
            return list[0][5:]

    def info( self ):
        import tools
        return tools.localerun( self.info_nolocale )

    def info_nolocale( self ):
        if not self.pkgname:
            return {}
        dict = {}

        shortname = self.getShortName( self.pkgname )

        #if self.ispackage():
        #    output = os.popen( 'pkginfo -l ' + shortname )
        output = os.popen( 'pkg info -r ' + shortname )
        for line in output:
            try:
                attr, value = line.split( ':', 1 )
                attr = attr.strip()
                value = value.strip()
                dict['package.' + attr] = value
            except:
                pass
        return dict

    def dbg_compareVer( self, ver1, ver2 ):
        if ver1 == ver2:
            return 0
        vstr1 = ver1.split( '.' )[-1]
        vstr2 = ver2.split( '.' )[-1]
        try:
            v1 = int( vstr1 )
            v2 = int( vstr2 )
            if v1 > v2 :
                return 1
            return - 1
        except:
            if vstr1 > vstr2:
                return 1
            return - 1

    def ispackage( self ):
        return ( os.system( 'pkginfo -q ' + self.pkgname ) == 0 )

if __name__ == '__main__':
    def usage():
        print sys.argv[0], '[-i | -a | -d | -A | -D] [driver_name [pkgname]] '
        sys.exit( 2 )

    try:
        if len( sys.argv ) == 4:
            p = Package( sys.argv[2], sys.argv[3] )
        elif len( sys.argv ) == 3:
            p = Package( sys.argv[2] )
        else:
            usage()
    except IndexError:
        usage()
    if sys.argv[1] == '-i':
        print p.info()
    elif sys.argv[1] == '-d':
        print p.uninstall()
    elif sys.argv[1] == '-D':
        print p.try_uninstall()
    elif sys.argv[1] == '-a':
        print p.install()
    elif sys.argv[1] == '-A':
        print p.try_install()
    else:
        usage()

"""
use case to test:
python Package.py -i hermon
"""
