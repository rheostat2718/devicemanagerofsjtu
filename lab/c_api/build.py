from distutils.core import setup, Extension
def builddi():
    setup( name = 'di', version = '1.0', ext_modules = [Extension( 'di', ['di.c'] )] )

def buildmodulec():
    setup( name = 'modulec', version = '1.0', ext_modules = [Extension( 'modulec', ['modulec.c'] )] )

if __name__ == '__main__':
    builddi()
    buildmodulec()
