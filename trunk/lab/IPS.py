#!/bin/env python
import os
import sys
import logging

import logger

class Package:
    """
    This class execute "pkg install | uninstall | list | info | search,
    provides an interface to PackageDrv
    
    __init__(self,name):
    select(self,list):
    validate(self,pkgname):
    update_pkglist(self,dict):
    search_pkglist(self):
    search(self):
    get_pkglist(self):
    clear_pkglist(self):
    GetNameList(self,lines,filter=None):
    GetFMRI(self,lines,filter=None):
    GetLatestVersion(self,lines,filter=None):
    try_install(self):
    try_uninstall(self):
    info(self):
    install( self , trial = False):
    uninstall( self , trial = False):
    getShortName(self,name):
    """

    def __init__(self, name, pkgname=None):
        self.name = name

        if pkgname:
            if self.validate(pkgname):
                self.pkgname = pkgname
                self.update_pkglist({self.name:self.pkgname})
            else:
                logging.debug('Discard ' + pkgname)
                pkgname = None

        if not pkgname:
            self.pkgname = self.search()
            print self.pkgname

    def select(self, list):
        #by default, choose the first, and it's always the only one
        if list:
            return list[0]

    def validate(self, pkgname):
        logging.debug("validate " + pkgname)
        lines = os.popen('pkg contents -t file ' + pkgname + '| grep "kernel\/drv"')
        for line in lines:
            filename = line[:-1].split('/')[-1]
            if filename == self.name:
                logging.info("find item " + line[:-1])
                return True
        logging.info(self.name + " not found in " + pkgname)
        return False

    def update_pkglist(self, dict):
        """
        update pkgdev.list if new data is in dict
        """
        olddict = {}
        try:
            for line in open('pkgdev.list', 'r').readlines():
                try:
                    key, value = line[:-1].split()
                    olddict[key] = value
                except ValueError:
                    continue
        except IOError:
            pass
        for key in dict.keys():
            olddict[key] = dict[key]
        f = open('pkgdev.list', 'w')
        for key in olddict.keys():
            f.write(key + ' ' + olddict[key] + '\n')
        f.close()

    def search_pkglist(self):
        """
        search pkgdev.list for self.name, return pkgname or None
        """
        logging.debug('search_pkglist ' + self.name)
        try:
            lines = open('pkgdev.list', 'r').readlines()
        except IOError:
            return None
        for line in lines:
            list = line.split()
            try:
                if self.name == list[0]:
                    ret = list[1]
                    return ret
            except IndexError :
                pass
        return None

    def search(self):
        logging.debug('search ' + self.name)
        pkgname = self.search_pkglist()
        if pkgname:
            return pkgname
        pkgname = self.get_pkglist()
        return pkgname

    def get_pkglist(self):
        """
        execute "pkg search -lr <name>", and get pkgname
        """
        logging.debug('get_pkglist ' + self.name)
        text = os.popen('pkg search -lr ' + self.name).readlines()
        list = self.GetNameList(text)
        if list:
            pkg = self.select(list)
            self.update_pkglist({self.name:pkg})
        else:
            pkg = None
        return pkg

    def clear_pkglist(self):
        """
        remove cache file
        return 0 as succeed, 1 as failed
        """
        try:
            open('pkgdev.list', 'w')
        except:
            return - 1
        return 0

    def GetNameList(self, lines, filter=None):
        """
        input: "pkg search ..." output
        output: pkgnamelist
        """
        logging.debug('getnamelist')
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
                (prefix, version) = package.split('@', 1)
                (type, name) = prefix.split(':/', 1)
                if not (name in pkg):
                    pkg.append(name)
                #pkg install always install the latest package when provided with name

            except ValueError:
                continue

        return pkg

    def GetFMRI(self, lines, filter=None):
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
                if not (package in pkg):
                    pkg.append(package)
            except ValueError:
                continue
        return pkg

    def GetLatestVersion(self, lines, filter=None):
        pkg = {}
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
                (prefix, version) = package.split('@', 1)

                if not (prefix in pkg):
                    pkg[prefix] = version
                elif self.dbg_compareFMRI(version, pkg[prefix]) > 0:
                    pkg[prefix] = version
            except ValueError:
                continue
        pkglist = []
        for prefix in pkg.keys():
            pkglist.append(prefix + '@' + pkg[prefix])
        logging.info(str(len(pkglist)) + ' matches:')
        return pkglist

    def try_install(self):
        return self.install(True)

    def try_uninstall(self):
        return self.uninstall(True)

    def install(self , trial=False):
        if trial:
            EXarg = '-n '
            logging.debug("try_install" + self.pkgname)
        else:
            EXarg = ' '
            logging.debug("install" + self.pkgname)

        try:
            ret = os.system('pfexec pkg install -v ' + EXarg + self.pkgname)
        except:
            ret = -1

        if ret == 0:
            logging.info('install finished')
        else:
            logging.error('install failed')
        return ret

    def uninstall(self, trial=False):
        if trial:
            EXarg = '-n '
            logging.debug("try_uninstall" + self.pkgname)
        else:
            EXarg = ' '
            logging.debug("uninstall" + self.pkgname)

        try:
            ret = os.system('pfexec pkg uninstall -v ' + EXarg + self.pkgname)
        except:
            ret = -1

        if ret == 0:
            logging.info('uninstall finished')
        else:
            logging.error('uninstall failed')
        return ret

    def getShortName(self, name):
        list = name.split('@')
        if len(list) == 1:
            return name
        else:
            return list[0][5:]

    def info(self):
        logging.debug('info')
        shortname = self.getShortName(self.pkgname)
        dict = {}
        output = os.popen( 'pkginfo -l ' + shortname )
#        output = os.popen('pkg info -r ' + shortname)
        for line in output:
            try:
                attr, value = line.split(':', 1)
                attr = attr.strip()
                value = value.strip()
                dict[attr] = value
            except:
                pass
        return dict



    def dbg_compareVer(self, ver1, ver2):
        if ver1 == ver2:
            return 0
        vstr1 = ver1.split('.')[-1]
        vstr2 = ver2.split('.')[-1]
        try:
            v1 = int(vstr1)
            v2 = int(vstr2)
            if v1 > v2 :
                return 1
            return - 1
        except:
            if vstr1 > vstr2:
                return 1
            return - 1

    def dbg_rebuild_index(self):
        # sometimes pkg asks you to rebuild its index, this function just run the script
        try:
            ret = os.system('pfexec pkg rebuild-index')
            return ret
        except:
            pass

    def verify(self):
        pass

    def check(self):
        return

    def ispackage():
        return (os.system('pfexec pkginfo -q ' + self.pkgname) == 0)

if __name__ == '__main__':
    def usage():
        print sys.argv[0], '[driver name [pkgname]]'

    logging.basicConfig(level=0)
    try:
        if len(sys.argv) == 3:
            p = Package(sys.argv[1], sys.argv[2])
        elif len(sys.argv) == 2:
            p = Package(sys.argv[1])
        else:
            usage()
    except IndexError:
        usage()
    print p.info()
#
