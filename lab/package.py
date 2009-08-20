#!/bin/env python2.6

import os
import sys
import string

def isPackage( pkgname ):
    return ( os.system( 'pfexec pkginfo -q ' + pkgname ) == 0 )


class Package():
    # A class that invokes pkg install / uninstall / list / search / info, managers pkg files
    def __init__( self, name, search, verbose ):
        if ( search == None ) | ( search == False ):
            self.name = name
        else:
            if search == 'remote':
                self.name = self.Find( name, verbose, '-r' )
            elif search == 'local':
                self.name = self.Find( name, verbose, '-l' )
            else:
                self.name = self.Find( name, verbose, '-lr' )
        self.Check()

    def Find( self , match, verbose, searcharg, filter = None ):
        if verbose:
            print 'Look for ' + match + ' in database'
            opt = ''
        else:
            opt = ' 2>/dev/null'
        try:
            output = os.popen( 'pkg search ' + searcharg + ' ' + match + opt ).readlines()
            pkg = {}
            for line in output:
                try:
                    index, action, value, name = line.split()
                    if verbose:
                        print line,
                    if action != 'file':
                        continue
                    if index == None:
                        continue
                    if ( filter != None ) & ( index != filter ):
                        continue
                    if ( name == '' ) | ( name == None ):
                        continue
                    if value.find( '/drv' ) == -1:
                        continue
                    ( prefix, ver ) = name.split( '@', 1 )
                    # always find latest packages
                    if not ( prefix in pkg ):
                        pkg[prefix] = ver
                    elif self.dbg_compareVer( ver, pkg[prefix] ) > 0:
                        pkg[prefix] = ver
                except:
                    continue

            pkglist = []
            for prefix in pkg.keys():
                pkglist.append( prefix + '@' + pkg[prefix] )

            if pkglist == []:
                if verbose:
                    print 'Package ' + match + ' not found'
                return
            if verbose:
                print 'Found ', len( pkglist ), ' matches:'
                for pkgname in pkglist:
                    print 'Package : ', pkgname
            return pkglist
        except:
            return

    def TryInstall( self, verbose = True, EXarg = '' ):
        self.Install( verbose, 'n' + EXarg )

    def Install( self , verbose = True, EXarg = '' ):
#FIXME:    if cannot install : return, print error message
        if verbose:
            arg = ' -v'
            opt = ' 2>/dev/null'
        else:
            arg = ' -q'
            opt = ''
        count = 0
        for pkgname in self.name:
            ret = -1
            if verbose:
                print 'Install package ', pkgname, ' :'
            try:
                ret = os.system( 'pkg install' + arg + EXarg + ' ' + pkgname + opt )
            except:
                pass
            if ret == 0:
                count = count + 1
                if verbose:
                    print 'Succeed!'
            else:
                if verbose:
                    print 'Failed!'
        return count

    def TryUninstall( self, verbose = True, EXarg = '' ):
        self.Uninstall( verbose, ' -n' + EXarg )

    def Uninstall( self, verbose = True, EXarg = '' ):
#FIXME:    check if we need -r, -r is very dangerous
        if verbose:
            arg = ' -v'
            opt = ''
        else:
            arg = ' -q'
            opt = ' 2>/dev/null'
        count = 0
        for pkgname in self.name:
            ret = -1
            if verbose:
                print 'Uninstall package ', pkgname, ' :'
            try:
                ret = os.system( 'pkg uninstall' + arg + EXarg + ' ' + pkgname + opt )
            except:
                pass
            if ret == 0:
                count = count + 1
                if verbose:
                    print 'Succeed!'
            else:
                if verbose:
                    print 'Failed!'
        return count

    def getInfo( self ):
        print self.name
        ret = []
        for name in self.name:
            shortname = name[5:].split( '@' )[0]
            dict = {}
            try:
                output = os.popen( 'pfexec pkginfo -l ' + shortname )
            except:
                pass
            for line in output:
                try:
                    attr, value = line.split( ':', 1 )
                    dict[attr] = value
                except:
                    pass
            ret.append( dict )
        return ret

    def Check( self ):
        return

    def dbg_compareVer( self, ver1, ver2 ):
        if ver1 == ver2:
            return 0
        vstr1 = ver1.split( '.' )[-1]
        vstr2 = ver2.split( '.' )[-1]
        try:
            v1 = string.atoi( vstr1 )
            v2 = string.atoi( vstr2 )
            if v1 > v2 :
                return 1
            return - 1
        except:
            if vstr1 > vstr2:
                return 1
            return - 1

    def dbg_rebuildIndex( self ):
        # sometimes pkg asks you to rebuild its index, we just invoke it
        try:
            ret = os.system( 'pkg rebuild-index' )
            return ret
        except:
            pass

if __name__ == '__main__':
    s = Package( 'pci-ide', True, True )
    print s.getInfo()

"""
extract from solaris's document
----------------------------------
# pkgchk package-name

import pkg? from python.setuptools?
"""
