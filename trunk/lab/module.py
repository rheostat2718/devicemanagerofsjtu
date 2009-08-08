from c_api.modulec import *
def getModid( name ):
    try:
        return getModuleId( name )
    except:
        return None

def getModinfoById( id ):
    try:
        dict = getModuleInfo( id )
        dict['INSTALLED'] = not ( dict['INSTALLED'] == 0 )
        dict['LOADED'] = not ( dict['LOADED'] == 0 )
        return dict
    except:
        pass

def getModinfoByName( name ):
    id = getModid( name )
    return getModinfoById( id )

def getPathList():
    return getModPath().split()

if __name__ == '__main__':
    print getPathList()
