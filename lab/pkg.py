import string
import os
import sys

def findPkg( pkgname, verbose = True ):
    if verbose:
        print 'Look for package ', pkgname
    try:
        pkglist = os.popen( ' pkg search -lr ' + pkgname ).readlines()
    except:
        pkglist = []
    pkgnamelist = getPackageNameList( pkglist )
    if verbose & ( pkgnamelist == [] ):
        print 'Package ', pkgname, ' not found'
        return
    if len( pkgnamelist ) == 1:
        if verbose:
            print 'Found Package : ', pkgnamelist[0]
        return pkgnamelist[0]
    if not verbose:
        return pkgnamelist[0]
    print 'Found ', len( pkgnamelist ), ' packages: '
    count = 0
    for name in pkgnamelist:
        print count, ' : ', name
    while True:
        i = string.atoi( raw_input( 'Choose one : ' ) )
        if i < len( pkgnamelist ):
            return pkgnamelist[i]
        else:
            print 'Failed!'

def getPackageNameList( pkglist , filter = None ):
    if pkglist == []:
        return []
    pkg = {}
    for line in pkglist[1:]:
        pkgfilter = line.split( ' ' )[0]
        if ( filter != None ) & ( pkgfilter != filter ):
            continue
        pkgnameitem = line.split( ' ' )[-1]
        ( pkgname, pkgver ) = pkgnameitem.split( '@', 1 )
        #Always find the latest package
        if not ( pkgname in pkg ):
            pkg[pkgname] = pkgver
        elif cmppkgver( pkgver, pkg[pkgname] ) > 0:
            pkg[pkgname] = pkgver
    pkgnamelist = []
    for key in pkg.keys():
        pkgnamelist.append( key + '@' + pkg[key] )
    return pkgnamelist

def cmppkgver( ver1, ver2 ):
    if ver1 == ver2:
        return 0
    vstr1 = ver1.split( '.' )[-1]
    vstr2 = ver2.split( '.' )[-1]
    try:
        vf1 = string.atof( vstr1 )
        vf2 = string.atof( vstr2 )
        if vf1 > vf2 :
            return 1
        else:
            return - 1
    except:
        if vstr1 > vstr2:
            return 1
        else:
            return - 1

def initialize():
    try:
        os.system( 'pkg rebuild-index' )
    except:
        pass

def printPackageInfo( pkgname ):
    import os
    os.system( 'pkg info ' + pkgname )

#may write getPackageInfo as {attr:value}

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
    s = findPkg( 'pci-ide' )
    if s != None:
        printPackageInfo( s )
