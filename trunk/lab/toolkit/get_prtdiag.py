import os, sys
"""
load prtdiag -v's output, get extra information...
"""
def sepstr( key, seps ):
    ret = []
    for i in range( len( seps ) ):
        ret.append( key[0:len( seps[i] )].strip() )
        key = key[( len( seps[i] ) + 1 ):]
    return ret

def get_prtdiag( f = None ):
    ret = {}
    if f == None:
        try:
            f = os.popen( 'prtdiag -v' )
        except:
            return ret
    lines = f.readlines()
    key, value = lines[0].split( ':', 1 )
    ret[key] = value[:-1]
    key, value = lines[1].split( ':', 1 )
    ret[key] = value[:-1]
    lines = lines[2:]
    while lines != []:
        while lines[0][:4] != '====':
            lines = lines[1:]
            if not lines:
                break
        if not lines:
            break
        keyword = lines[0].replace( '=', '' ).strip()
        items = []
        lines = lines[1:]
        if ( keyword == 'Upgradeable Slots' ) | ( keyword == 'Processor Sockets' ) | ( keyword == 'Memory Device Sockets' ):
            lines = lines[1:]
            seps = lines[1].split()
            keys = sepstr( lines[0], seps )
            lines = lines[2:]
            while lines[0].strip() != '':
                item = {}
                values = sepstr( lines[0], seps )
                for i in range( len( values ) ):
                    item[keys[i]] = values[i]
                lines = lines[1:]
                if not lines:
                    break
            items.append( item )
        if ( keyword == 'On-Board Devices' ):
            while lines[0].strip() != '':
                items.append( lines[0].strip() )
                lines = lines[1:]
                if not lines:
                    break
        #print items
        ret[keyword] = items
    return ret

if __name__ == '__main__':
    f = open( 'prtdiag.txt', 'r' )
    print get_prtdiag( f )
