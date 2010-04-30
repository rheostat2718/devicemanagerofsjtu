import modulec

if __name__ == '__main__':
    print 'test getModuleInfo()'
    print 'module 250 info', modulec.getModuleInfo( 250 )
    try:
        print 'module 1234 info', modulec.getModuleInfo( 1234 )
    except SystemError as e:
        print 'expect SystemError as: ', e

    print 'test getModuleId()'
    print 'id for ipc', modulec.getModuleId( 'ipc' )
    print 'id for asdf', modulec.getModuleId( 'asdf' )

    print 'test getMajorName()'
    print 'name of major number 4', modulec.getMajorName( 4 )
    try:
        print 'name of major number 1234', modulec.getMajorName( 1234 )
    except SystemError as e:
        print 'expect SystemError as: ', e

    print 'test getModPath'
