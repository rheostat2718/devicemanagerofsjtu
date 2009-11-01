import os, sys

def get_psrinfo():
    lines = os.popen('psrinfo -v').readlines()
    return read_psrinfo(lines)

def read_psrinfo():
    keyword = ['virtual processor number', #id
               'status', #one of the following: ONLINE NO-INTR SPARE OFFLINE FAULT POWERED OFF
               'last changed time',
               'processor type','floating point unit type','clock speed']
    return

if __name__ == '__main__':
    print get_psrinfo()
    # debug: print read_psrinfo( open( 'psrinfo.txt', 'r' ).readlines() )
