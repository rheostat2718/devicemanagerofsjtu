#!/bin/env python2.6

import os
import sys
import string

class Package():
    # A class that invokes pkg install / uninstall / list / search / info, managers pkg files
    def __init__( self, name, search, verbose ):
        if not search:
            self.name = name
        else:
            self.name = self.Find( name, verbose )
        self.Check()

    def Find( self , match, verbose, filter = None ):
        if verbose:
            print 'Look for ', match, ' in database'
            opt = ''
        else:
            opt = ' 2>/dev/null'
        try:
            output = os.popen( 'pkg search -lr ' + match + opt ).readlines()
            if verbose:
                for line in output:
                    print line
            pkg = {}
            for line in output[1:]:
                resulttype = line.split( ' ' )[0]
                name = line.split( ' ' )[-1]
                if ( filter != None ) & ( resulttype != filter ):
                    continue
                ( prefix, ver ) = name.split( '@', 1 )
                # always find latest packages
                if not ( prefix in pkg ):
                    pkg[prefix] = ver
                elif self.dbg_compareVer( ver, pkg[prefix] ) > 0:
                    pkg[prefix] = ver

            pkglist = []
            for prefix in pkg.keys():
                pkglist.append( prefix + '@' + pkg[prefix] )

            if pkglist == []:
                if verbose:
                    print 'Package ', match, ' not found'
                return
            else:
                if verbose:
                    print 'Found ', len( pkglist ), ' matches:'
            for pkgname in pkglist:
                print 'Package : ', pkgname
            return pkglist
        except:
            return

    def Install( self ):
        return

    def Uninstall( self ):
        return

    def getInfo( self ):
        try:
            output = os.popen( 'pkg info ', self.name )
#FIXME:attr and value are Language specific....
            dict = {}
            for line in output:
                ( attr, value ) = line.split( ':' )
                dict[attr] = value
            return dict
        except:
            pass

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

def installPackage( pkgname, verbose = True ):
    import os
    if not verbose:
        option = '-q '
    else:
        option = ' '
    ret = os.system( 'pkg install ' + option + pkgname )
    if ret < 0 & verbose:
            print 'Installion Failed'
    return ret

def uninstallPackage( pkgname, verbose = True ):
    import os
    if not verbose:
        option = '-rq '
    else:
        option = '-r '
    ret = os.system( 'pkg uninstall ' + option + pkgname )
    if ret < 0 & verbose:
        print 'Uninstallion Failed'
    return ret

if __name__ == '__main__':
    s = Package( 'pci-ide', True, True )
    print s.getInfo()
"""
安装驱动程序。
# pkgadd [-d] device package-name
-d device 用于标识包含软件包的设备路径名。
package-name 用于标识包含设备驱动程序的软件包名称

检验软件包是否已正确添加。
# pkgchk package-name
如果正确安装了软件包，则系统提示不会返回任何响应
"""
