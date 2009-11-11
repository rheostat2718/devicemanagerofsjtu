#!/bin/env python2.6

import os
import sys
import traceback
from c_api.modulec import *

class BaseDriver():
    """
    Base type of all Driver items
    """
    def __init__(self, drvname):
        self.drvname = drvname

    def info(self):
        dict = {'name':self.drvname} #short-name
        return dict
    
    def install(self):
        pass
    
    def uninstall(self):
        pass
    
class LocatedDriver(BaseDriver):
    """
    Automatically find driver file
    """
    def __init__(self,drvname):
        BaseDriver.__init__(self,drvname);
        self.collect_env()
        if (self.drvname.find(os.path.sep) != -1):
            list = self.drvname.rsplit(os.path.sep,1)
            self.drvname = list[-1];
            self.path = list[0]
        else:
            self.path = ''
            self.AutoLocate()
    
    def getFullPath(self):
        return self.path + self.drvname
    
    def collect_env(self):
        """
        invoke a series of opensolaris command-line tools to
        detect device driver locations
        """
        output = os.popen('isainfo -b').readlines()[0]
        if output[:2] == '64':
            self.env_bit = 64
        elif output[:2] == '32':
            self.env_bit = 32
        self.dev_subpath = os.popen('isainfo -k').readlines()[0]
        self.dev_path = os.popen('arch -k').readlines()[0]            

    def IsExist(self):
        return os.path.exists(self.getFullPath());
    
    def ManualLocate(self,path):
        self.path = path
    
    def AutoLocate(self):
        """
        Automatically find the path of device file
        find in:
        /kernel/drv /usr/kernel/drv /platform/xxxx/kernel/drv ... /amd64
        /etc/system -> moddir
        """
        self.path = ''
        dirlist = ['/kernel/drv','usr/kernel/drv','/platform/'+self.dev_path+'/kernel/drv','']
        for directory in dirlist:
            if not directory:
                break
            if self.dev_subpath:
                finddir = directory + '/'+self.dev_subpath+'/'
            else:
                finddir = directory + '/'
            if os.path.exists(finddir+self.drvname):
                self.path = finddir
                return
        #default path
        self.path = dirlist[0]+'/'

    def info(self):
        dict = BaseDriver.info(self)
        dict['devfs path'] = self.path
        dict['full path'] = self.getFullPath()
        dict['file exists?'] = self.IsExist()
        return dict
        
class IPSMixin():
    def __init__(self):
        pass
            
class Driver(LocatedDriver):
    def __init__( self, drvname ):
        LocatedDriver.__init__(self,drvname);
        try:
            self.defaultdrvpath, self.defaultconfpath = getFirstDriverPathConf()
        except:
            self.defaultdrvpath = ''
            self.defaultconfpath = ''

    def isInstalled( self ):
        return ( self.getInfo()['INSTALLED'] != 0 )

    def isLoaded( self ):
        return ( self.getInfo()['LOADED'] != 0 )

    def getAllDriverPath( self ):
        ret = []
        for ( a, b ) in findDrvConf( self.drvname ):
            ret.append( a )
        return ret

    def getFirstDriverConfPath( self ):
        return self.getAllDriverConfPath()[0]

    def getFirstDriverPath( self ):
        return self.getAllDriverPath()[0]

    def getAllDriverConfPath( self ):
        """
            Having more than 2 subdir is completely possible, e.g. some on 32b system and others on 64b system
        """
        subdirlist = []
        mapdict = {'amd64':'amd64', 'sparcv9':'sparcv9', 'i386':'.'}
        for name in os.popen( 'arch -k' ).readline().split():
            subdirlist.append( mapdict[name] )
        ret = []
        for currdir in getModPath().split:
            for subdir in subdirlist:
                drvname = currdir + os.path.sep + 'drv' + os.path.sep + subdir + os.path.sep + self.drvname
                if os.path.isfile( drvname ):
                    # driver.conf in .../drv
                    confname = currdir + os.path.sep + 'drv' + os.path.sep + self.drvname + '.conf'
                    if os.path.isfile( confname ):
                        ret.append( ( drvname, confname ) )
                        #FIXME: I don't know whether should return None or deprecate it
                    else:
                        ret.append( ( drvname, None ) )
        return ret

    def dbg_loadModule( self, verbose = True ):
        """
        First try to remove old modules before we proceed, then we load it
        """
        if not self.isInstalled():
            if verbose:
                print "Module %s not found" % self.drvname
            return
        if self.isLoaded():
            try:
                ret = self.dbg_unloadModule( verbose )
            except:
                if verbose:
                    print 'Cannot unload old module : ', self.drvname
        if  self.isLoaded():
            if verbose:
                print 'Cannot unload old module : ', self.drvname
                return
        if verbose:
            print "Module ", self.drvname, ':', self.defaultdrvpath, ':'
            opt = ''
        else:
            opt = ' 2>/dev/null'

        ret = os.popen( 'modinst ' + self.defaultdrvpath + opt )
        if verbose:
            if ret != 0:
                print 'Failed'
            else:
                print 'Succeed'
        return ret

    def dbg_unloadModule( self, verbose = True ):
        if not self.isInstalled():
            if verbose:
                print "Module %s not found" % self.drvname
            return
        if not self.isLoaded():
            print 'Module %s not loaded' % self.drvname
            return
        else:
            idno = self.getId()
        if idno == None:
            print 'Module %s not loaded' % self.drvname
            return
        if verbose:
            print "Module :", self.drvname, ': Id', idno
        ret = os.system( 'modunload -i ' + str( idno ) )
        if verbose:
            if ret != 0:
                print 'Failed'
            else:
                print 'Succeed'
        return ret

    def dbg_touchReconf():
        """
        just tell the system to find new hardware in the next boot,
        execute it to setup it manually
        """
        return os.system( 'touch /reconfigure' )

    def Backup( self ):
        return

    def Restore( self ):
        return

    def isBackup( self ):
        pass

    def getInfo( self, pkg = False ):
        id = self.getId()
        if id == None:
            return
        dict = LocatedDriver.info(self)
        try:
            info = getModuleInfo( id )
            for key in dict.keys():
                info[key] = dict[key]
            #pkg search is really slow,disable it ...
            if pkg == True:
                info['package'] = self.getPackageInfo()
            else:
                info['package'] = 'Unknown'
            return info
        except:
            pass

    def getId( self ):
        try:
            return getModuleId( self.drvname )
        except:
            pass

    def Install( self, verbose = True, InstallFromPackage = True, arg = None ):
        """
        We can use pkg install / pkgadd to install drivers,
        and we may use shell command, as written in Solaris document 819-7057.pdf
        """
        try:
            if InstallFromPackage:
                """
                Install from file pkgname, if pkgname is None, then we search in PKG's database and choose the latest package
                """
                if arg != None:
                    self.Install_Pkg( verbose, arg )
                else:
                    self.Install_Search( verbose )
            else:
                if arg == None:
                    if verbose:
                        print 'You need to specify files to install'
                    return
                elif len( arg ) == 1:
                    if arg[0][-4:] == '.pkg' :
                        self.Install_Pkg( verbose, arg[0] )
                    else:
                        if verbose:
                            print 'You need to specify two or more files, or an package.'
                        return
                else:
                    self.Install_Cpy( verbose, arg )
        except:
            pass

    def Install_Pkg( self, verbose, pkgname ):
        if os.path.isfile( pkgname ):
            if verbose:
                print 'Install from ', pkgname
                opt = ''
            else:
                opt = ' 2>/dev/null'
            ret = os.system( 'pkgadd -d ' + self.drvname + ' ' + pkgname + opt )
            return ret
        else:
            print 'Cannot find ', pkgname
            return

    def Install_Cpy( self, verbose, args ):
        """
        install without pkgadd, the driver and its configure file must be in the same directory
        """
        USR_KERNEL_DRV = r'/usr/kernel/drv'
        drvlist = []
        conflist = []
        fname.split()
        if verbose:
            opt = ''
        else:
            opt = ' /dev/null'
        for fname in args:
            if not os.path.exists( fname ):
                if verbose:
                    print 'File ', fname, ' does not exist'
                    return
            #TODO: more restruction on fname, only 26 lower alphabetic, 10 digit _
            if fname.find( '.' ) != None:
                if fname[-5:] != '.conf':
                    if verbose:
                        print fname, ' is neither a driver or driver.conf, installion abort'
                    return
                elif fname[:-5].find( '.' ) != None:
                    if verbose:
                        print fname, ' is neither a driver or driver.conf, installion abort'
                    return
                else:
                    path, name = os.path.split( fname )
                    if name in conflist:
                        continue
                    conflist.append( name )
            else:
                path, name = os.path.split( fname )
                if name in drvlist:
                    continue
                drvlist.append( name )
        for name in drvlist:
            if not ( ( name + '.conf' ) in conflist ):
                print "driver and configure doesn't match :", name, ' .conf not found.'
                return
        for fname in args:
            if verbose:
                print 'cp ', fname,
            path, name = os.path.split( fname )
            if name in drvlist:
                if verbose:
                    print ' to ', USR_KERNEL_DRV + os.path.sep, subdir, os.path.sep
                ret = os.system( "cp " + fname + ' ' + USR_KERNEL_DRV + os.path.sep + subdir + os.path.sep + opt )
            else:
                if verbose:
                    print ' to ', USR_KERNEL_DRV + os.path.sep
                ret = os.system( "cp " + fname + ' ' + USR_KERNEL_DRV + os.path.sep + opt )
            if ret != 0:
                if verbose:
                    print 'Operation Failed.'
                return
        for name in drvlist:
            if verbose:
                print 'add_drv :', name,
            ret = os.system( 'add_drv ' + name + opt )
            if verbose:
                if ret < 0:
                    print 'Failed'
                    #If this one fails, go on ...
                else:
                    print 'Succeed'
#TODO: add_drv does not support STREAM devices
#(816-4855.pdf) reference : sad, autopush
        self.dbg_touchReconf()
        if verbose:
            print 'Changes will take effect during your next reboot'
        return 0

    def Install_Search( self, verbose ):
        try:
            import package
            driverPkg = package.Package( self.drvname, search = 'remote', verbose = verbose )
            if driverPkg.name == None:
                if verbose:
                    print 'Cannot find related package'
                    return
            return driverPkg.Install( verbose )
        except:
            if verbose:
                exc_info = sys.exc_info()
                print exc_info[0]
                print exc_info[1]
                traceback.print_tb( exc_info[2] )
                return

    def Update( self ):
        return

    def Uninstall( self, verbose = True, removeFromPackage = True, arg = None ):
        try:
            if removeFromPackage:
                if arg:
                    self.Uninstall_Pkg( verbose, arg )
                else:
                    self.Uninstall_Search( verbose )
            else:
                if arg == None:
                    if verbose:
                        print 'You need to specify files to install'
                    return
                else:
                    self.Uninstall_Cpy( verbose, arg )
        except:
            pass

    def Uninstall_Pkg( self, verbose, pkgname ):
        if os.path.isfile( pkgname ):
            if verbose:
                print 'Uninstall from ', pkgname
                opt = ''
            else:
                opt = ' 2>/dev/null'
#TODO: find out the cmd
#            ret = os.system('pkgrem '+pkgname+opt)
            return ret
        else:
            print 'Cannot find ', pkgname
            return

    def Uninstall_Cpy( self, verbose, arg ):
        if verbose:
            opt = ''
        else:
            opt = ' /dev/null'
        if verbose:
            print 'rem_drv :', self.drvname,
        ret = os.system( 'rem_drv ' + self.drvname + opt )
        if verbose:
            if ret < 0:
                print 'Failed'
                #If this one fails, go on ...
            else:
                print 'Succeed'
        for fname in args:
            if verbose:
                print 'rm ', fname
            ret = os.system( "rm -f " + fname + opt )
            if verbose:
                if ret != 0:
                    print 'Failed'
                    #If this one fails, go on ...
                else:
                    print 'Succeed'

    def Uninstall_Search( self, verbose ):
        try:
            import package
            driverPkg = package.Package( self.drvname, search = 'local', verbose = verbose )
            if driverPkg.name == None:
                if verbose:
                    print 'Cannot find related package'
                return
            return driverPkg.Uninstall( verbose )
        except:
            if verbose:
                exc_info = sys.exc_info()
                print exc_info[0]
                print exc_info[1]
                traceback.print_tb( exc_info[2] )
                return

    def getPackageInfo( self ):
        try:
            import package
#TODO: impove search
            driverPkg = package.Package( self.drvname, search = True, verbose = False )
            if driverPkg.name == None:
                return
            return driverPkg.getInfo()
        except:
            if verbose:
                exc_info = sys.exc_info()
                print exc_info[0]
                print exc_info[1]
                traceback.print_tb( exc_info[2] )
                return

if __name__ == '__main__':
    if len( sys.argv ) < 4:
        print "Usage: [python2.6] drv.py {install | uninstall | info} drvname [-q | -v]"
    else:
        if sys.argv[1] == 'install':
            Driver( sys.argv[2] ).Install( ( sys.argv[3] == '-v' ), True )
        if sys.argv[1] == 'uninstall':
            Driver( sys.argv[2] ).Uninstall( ( sys.argv[3] == '-v' ), True )
        if sys.argv[1] == 'info':
            print Driver( sys.argv[2] ).getInfo( True )

"""
TESTED:
drv.py install sppp -v
drv.py install sppp -q
drv.py uninstall sppp -v
drv.py uninstall sppp -q
drv.py info sppp
TODO:
2
"""
