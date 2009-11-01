import os
import sys

class Package():
    """
    this class invokes pkg install / uninstall / list / search / info,
    manages IPS operations
    """
    def __init__(self, name, verbose):
        self.name = name
        self.pkgname = None
        self.verbose = verbose
    
    def GetNameList(self,lines):
        pkg = []
        for line in lines:
            if verbose:
                print line,
            try:
                index,action,value,package = line.split()
                if action != 'file':
                    continue
                if (not index) | (not package):
                    continue
                if filter & (index != filter):
                    continue
                if value.find('/drv') == -1:
                    continue #make sure it is a driver
                (prefix,version) = package.split('@',1)
                (type,name) = prefix.split(':/',1)
                
                if not (name in pkg):
                    pkg.append(name)
                #pkg install always install the latest package when provided with name
            except:
                continue
        return pkg
    
    def GetFMRI(self,lines):
        pkg = []
        for line in lines:
            if verbose:
                print line,
            try:
                index,action,value,package = line.split()
                if action != 'file':
                    continue
                if (not index) | (not package):
                    continue
                if filter & (index != filter):
                    continue
                if value.find('/drv') == -1:
                    continue #make sure it is a driver
                if not ( package in pkg ):
                    pkg.append(package)
            except:
                continue
        return pkg
    
    def GetLatestVersion(self,lines):
        pkg = {}
        for line in lines:
            if verbose:
                print line,
            try:
                index,action,value,package = line.split()
                if action != 'file':
                    continue
                if (not index) | (not package):
                    continue
                if filter & (index != filter):
                    continue
                if value.find('/drv') == -1:
                    continue #make sure it is a driver
                (prefix,version) = package.split('@',1)

                if not ( prefix in pkg ):
                    pkg[prefix] = version
                elif self.dbg_compareFMRI( version, pkg[prefix] ) > 0:
                    pkg[prefix] = version
            except:
                continue
        pkglist = []
        for prefix in pkg.keys():
            pkglist.append( prefix + '@' + pkg[prefix] )
        if verbose:
            print 'Found ', len( pkglist ), ' matches:'
            for pkgname in pkglist:
                print 'Package name: ', pkgname
        return pkglist
    
    def Search(self, arg = '-lr', filter = None):
        """
        arg : arguments used in pkg search
        '-r','-l','-lr', and ''
        """
        opt = ''
        if self.verbose:
            print 'pkg search',self.name,arg
        else:
            opt = ' 2>/dev/null'
        output = os.popen('pkg search'+arg+' '+match+opt).readlines()
        return self.GetNameList(output)
    

    def TryInstall( self, verbose = True, EXarg = '' ):
        self.Install( verbose, 'n' + EXarg )

    def Install( self , verbose = True, EXarg = '' ):
#FIXME:    if cannot install : return, print error message
        if verbose:
            arg = ' -v'
            opt = ' 2>/dev/null'
        else:
            arg = ' -q'
            opt = ''
        count = 0
        for pkgname in self.name:
            ret = -1
            if verbose:
                print 'Install package ', pkgname, ' :'
            try:
                ret = os.system( 'pfexec pkg install' + arg + EXarg + ' ' + pkgname + opt )
            except:
                pass
            if ret == 0:
                count = count + 1
                if verbose:
                    print 'Succeed!'
            else:
                if verbose:
                    print 'Failed!'
        return count

    def TryUninstall( self, verbose = True, EXarg = '' ):
        self.Uninstall( verbose, ' -n' + EXarg )

    def Uninstall( self, verbose = True, EXarg = '' ):
#FIXME:    check if we need -r, -r is very dangerous
        if verbose:
            arg = ' -v'
            opt = ''
        else:
            arg = ' -q'
            opt = ' 2>/dev/null'
        count = 0
        for pkgname in self.name:
            ret = -1
            if verbose:
                print 'Uninstall package ', pkgname, ' :'
            try:
                ret = os.system( 'pfexec pkg uninstall' + arg + EXarg + ' ' + pkgname + opt )
            except:
                pass
            if ret == 0:
                count = count + 1
                if verbose:
                    print 'Succeed!'
            else:
                if verbose:
                    print 'Failed!'
        return count

    def getInfo( self ):
        print self.name
        ret = []
        for name in self.name:
            shortname = name[5:].split( '@' )[0]
            dict = {}
            try:
                output = os.popen( 'pfexec pkginfo -l ' + shortname )
            except:
                pass
            for line in output:
                try:
                    attr, value = line.split( ':', 1 )
                    dict[attr] = value
                except:
                    pass
            ret.append( dict )
        return ret

    def Check( self ):
        return

    def dbg_compareVer( self, ver1, ver2 ):
        if ver1 == ver2:
            return 0
        vstr1 = ver1.split( '.' )[-1]
        vstr2 = ver2.split( '.' )[-1]
        try:
            v1 = int( vstr1 )
            v2 = int( vstr2 )
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
            ret = os.system( 'pfexec pkg rebuild-index' )
            return ret
        except:
            pass

if __name__ == '__main__':
    s = Package( 'pci-ide', True, True )
    print s.getInfo()

"""
usage : pkgchk package-name
"""

def isPackage( pkgname ):
    return ( os.system( 'pfexec pkginfo -q ' + pkgname ) == 0 )
def verify():
    pass

