import modulec

def test():
    print 'test ( 1 / 4 ) getModuleInfo()'
    print 'module 250 info', modulec.getModuleInfo( 250 )
    try:
        print 'module 1234 info', modulec.getModuleInfo( 1234 )
    except SystemError:
        print 'caught expecting SystemError'

    print 'test ( 2 / 4 ) getModuleId()'
    print 'id for ipc', modulec.getModuleId( 'ipc' )
    print 'id for asdf', modulec.getModuleId( 'asdf' )

    print 'test ( 3 / 4 ) getMajorName()'
    print 'name of major number 4', modulec.getMajorName( 4 )
    try:
        print 'name of major number 1234', modulec.getMajorName( 1234 )
    except SystemError:
        print 'caught expecting SystemError'

    print 'test ( 4 / 4 ) getModPath(), getModPathLen()'
    print 'module path len', modulec.getModPathLen()
    print 'module path', modulec.getModPath()

if __name__ == '__main__':
    test()

