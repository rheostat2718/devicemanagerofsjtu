#!/bin/env python
import os
import sys
import logging

import logger

class Package:
    """
    this class invokes "pkg install / uninstall / list / info",
    as a glue layer, manages package operations
    """
    def __init__(self, name):
        self.name = name
        self.pkgnamelist = self.Search()
        if self.pkgnamelist:
            self.pkgname = self.pkgnamelist[0]
        else:
            self.pkgname = None
        #it seems always find one device
        if self.pkgname:
            logging.info('Find '+self.pkgname)
        else:
            logging.error('Cannot find package matches '+self.name)
        
    def Search(self):
        logging.debug('search for '+self.name)
        devlist = self.get_devlist()
        
    
    def GetNameList(self,lines,filter):
        pkg = []
        for line in lines:
            line = line[:-1]
            logging.info(line)
            try:
                llist = line.split()
                package = llist[-1]
                value = llist[-2]
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

    def get_devlist(self):
        """
        invoke pkg search self.name
        """
        text = os.popen('pkg search -lr '+self.name).readlines()
        pkgnamelist = GetNameList(text)
        return pkgname

    def update_devlist(self,dict):
        """
        update pkgdev.list if new data(list) is available
        """
        old = open('pkgdev.list','r').readlines()
        f = open('pkgdev.list','w')
        f.write(old)
        for key in dict.keys():
            f.write(key+' '+dict[key]+'\n')
        f.close()

    def search_devlist(self):
        """
        search pkgdev.list for self.name
        """
        line = open('pkgdev.list','a').readlines()
        for line in lines:
            list = line.split()
            try:
                if self.name == list[0]:
                    ret = list[1]
                    return ret
            except IndexError :
                pass
        return None

    def clear_devlist(self,name):
        os.system('rm pkgdev.list')
        open('pkgdev.list','w')

"""
usage : pkgchk package-name
"""

def isPackage( pkgname ):
    return ( os.system( 'pfexec pkginfo -q ' + pkgname ) == 0 )

def verify():
    pass

if __name__ == '__main__':
    update_devinfo()

#