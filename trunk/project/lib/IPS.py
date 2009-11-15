import os
import sys

class Package():
    """
    this class invokes pkg install / uninstall / list / search / info,
    manages IPS operations
    """
    def __init__(self, name):
        self.name = name
        self.pkgname = self.Search()
        print self.pkgname
        
    def Search(self, arg = '-lr', filter = None):
        """
        arg : arguments used in pkg search
        '-r','-l','-lr', and ''
        """
        print 'search for ',self.name,arg
        output = os.popen('pkg search '+arg+' '+self.name).readlines()
        return self.GetNameList(output)
    
    def GetNameList(self,lines,filter = None):
        pkg = []
        for line in lines:
            line = line[:-1]
            print line
            try:
                index, action, value, package = line.split()
                if (action != 'file') | (not index) | (not package):
                    continue
                if filter and (index != filter):
                    continue
                if value.find('/drv') == -1:
                    continue #make sure it is a driver
                (prefix, version) = package.split('@',1)
                (type,name) = prefix.split(':/',1)
                if not (name in pkg):
                    pkg.append(name)
                #pkg install always install the latest package when provided with name
                
            except ValueError:
                continue
                
        return pkg
    
    def GetFMRI(self,lines,filter=None):
        pkg = []
        for line in lines:
            line = line[:-1]
            print line
            try:
                index, action, value, package = line.split()
                if (action != 'file') | (not index) | (not package):
                    continue
                if filter and (index != filter):
                    continue
                if value.find('/drv') == -1:
                    continue #make sure it is a driver
                if not ( package in pkg ):
                    pkg.append(package)
            except ValueError:
                continue
        return pkg
    
    def GetLatestVersion(self,lines):
        pkg = {}
        for line in lines:
            line = line[:-1]
            print line
            try:
                index,action,value,package = line.split()
                if (action != 'file') | (not index) | (not package):
                    continue
                if filter and (index != filter):
                    continue
                if value.find('/drv') == -1:
                    continue #make sure it is a driver
                (prefix,version) = package.split('@',1)

                if not ( prefix in pkg ):
                    pkg[prefix] = version
                elif self.dbg_compareFMRI( version, pkg[prefix] ) > 0:
                    pkg[prefix] = version
            except ValueError:
                continue
        pkglist = []
        for prefix in pkg.keys():
            pkglist.append( prefix + '@' + pkg[prefix] )
        print 'Found ', len( pkglist ), ' matches:'
        for pkgname in pkglist:
            print 'Package name: ', pkgname
        return pkglist
    
    def TryInstall( self, EXarg = '' ):
        self.Install( ' -n ' + EXarg )

    def Install( self , EXarg = '' ):
#FIXME:    if cannot install : return, print error message
        arg = ' -v'
        count = 0
        for pkgname in self.pkgname:
            ret = -1
            try:
                ret = os.system( 'pfexec pkg install' + arg + EXarg + ' ' + pkgname )
            except:
                pass
            if ret == 0:
                count = count + 1
                print 'Succeed!'
            else:
                print 'Failed!'
        return count

    def TryUninstall( self, EXarg = '' ):
        self.Uninstall( ' -n' + EXarg )

    def Uninstall( self, EXarg = '' ):
#FIXME:    check if we need -r, -r is very dangerous
        arg = ' -v'
        count = 0
        for pkgname in self.pkgname:
            ret = -1
            try:
                ret = os.system( 'pfexec pkg uninstall' + arg + EXarg + ' ' + pkgname)
            except:
                pass
            if ret == 0:
                count = count + 1
                print 'Succeed!'
            else:
                print 'Failed!'
        return count

    def getShortName(self,name):
        list = name.split('@')
        if len(list) == 1:
            return name
        else:
            return list[0][5:]
    
    def getInfo( self ):
#        print self.name
        ret = []
        for name in self.pkgname:
            shortname = self.getShortName(name)
            dict = {}
            output = os.popen( 'pfexec pkginfo -l ' + shortname )
            for line in output:
                try:
                    attr, value = line.split( ':', 1 )
                    dict[attr] = value[:-1]
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

