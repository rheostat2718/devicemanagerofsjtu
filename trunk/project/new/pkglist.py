import os, sys

outputfile = "pkgbuff"
listfile = 'pkglist'

class StaticData( object ):
    pkgDict = {} #only one instance

def getDrvList( verbose = False ):
    """
    use pkg search to get all available package names
    """
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

def dumpList( filename = listfile, list = [] ):
    """
    customize string list dumper (test only)
    """
    f = open( filename, 'w' )
    for item in list:
        f.write( item + '\n' )
    f.close()

def getContentDict( list , verbose = False ):
    """
    use pkg content to collect drv-pkg relation
    """
    dict = StaticData.pkgDict
    dict.clear()
    count = 0
    total = len( list )
    for pkgname in list:
        count += 1
        if verbose:
            print '(', count, '/', total, ')', 'pkg contents', pkgname, '|',
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
            print '#'
        print '|'
    return dict

def dumpDict( filename = outputfile, dict = StaticData.pkgDict ):
    """
    dump dict into file
    """
    #print dict
    f = open( filename, 'w' )
    for key in dict.keys():
        f.write( key + ' ' + dict[key] + '\n' )
    f.close()

def loadDict( filename = outputfile ):
    """
    call loadDict to get cached package-driver infomation.
    """
    #create file if it is not exist
    os.system( "touch " + filename );
    try:
        data = open( filename, 'r' ).readlines()
    except IOError:
        return StaticData.pkgDict

    dict = StaticData.pkgDict
    dict.clear()
    for line in data:
        if line[0] == '#':
            continue
        ( key, value ) = line.strip().split( ' ', 1 )
        dict[key] = value

    return dict

def fastload():
    """
    try use pkgDict at first 
    """
    if not StaticData.pkgDict:
        StaticData.pkgDict = loadDict()
    return StaticData.pkgDict

def combineDict( userdict, removeChange = False ):
    """
    update cacheddict with user-defined data, changes are made in cacheddict
    """
    for key in userdict.keys():
        StaticData.pkgDict[key] = userdict[key]
    if removeChange:
        userdict = {}

def removeKey( keylist ):
    """
    remove a list of keys from dict
    """
    for key in keylist:
        if key in StaticData.pkgDict.keys():
            StaticData.pkgDict.pop( key )

def removeDump():
    dumpDict( outputfile, {} )

def run():
    """
    very slow process...
    should use a new thread...
    """
    p = getDrvList( True )
    q = getContentDict( p, True )
    dumpDict( outputfile, q )
    combineDict( q )

#by default load pkgDict     
fastload()

if __name__ == '__main__':
    run()

