import os, sys

outputfile = "pkgbuff"
dict = None

"""
use pkg search to get all available package names
"""
def getDrvList( verbose = False ):
    if verbose:
        print 'pkg search'
    text = os.popen( 'pkg search -lr drv' ).readlines()
    list = []
    for line in text:
        line = line.strip().split()[-1].split( '@' )[0][5:]
        if not line in list:
            list.append( line )
    list.sort()
    return list

"""
customize string list dumper (test only)
"""
def dumpList( filename, list ):
    f = open( filename, 'w' )
    for item in list:
        f.write( item + '\n' )
    f.close()

def getContentDict( list , verbose = False ):
    dict = {}
    count = 0
    total = len( list )
    for pkgname in list:
        count += 1
        if verbose:
            print '(', count, '/', total, ')', 'pkg contents', pkgname, 'found : ', len( dict.keys() )

        text = os.popen( 'pkg contents -r -t file ' + pkgname ).readlines()
        for line in text:
            if line.find( r'kernel/drv' ) == -1:
                continue
            # get driver name
            line = line.strip().split( '/' )[-1]
            # exclude configure file
            if line.find( '.' ) != -1:
                continue

            dict[line] = pkgname

    return dict

def dumpDict( filename, dict ):
    f = open( filename, 'w' )
    for key in dict.keys():
        f.write( key + ' ' + dict[key] + '\n' )
    f.close()

"""
call loadDict to get cached package-driver infomation.
"""
def loadDict( filename ):
    data = open( filename, 'r' ).readlines()
    ret = {}
    for line in data:
        ( key, value ) = line.strip().split( ' ', 1 )
        ret[key] = value
    return ret

def combineDict( cacheddict, userdict, removeChange = False ):
    """
    update cacheddict with user-defined data, changes are made in cacheddict
    """
    for key in userdict.keys():
        cacheddict[key] = userdict[key]
    if removeChange:
        userdict = {}

def removeKey( cacheddict, keylist ):
    """
    remove a list of keys from dict
    """
    for key in keylist:
        if key in cacheddict.keys():
            cacheddict.pop( key )
"""
very slow process...
should use a new thread...
"""
def run():
    p = getDrvList( True )
    q = getContentDict( p, True )
    dumpDict( outputfile, q )

if __name__ == '__main__':
    run()

