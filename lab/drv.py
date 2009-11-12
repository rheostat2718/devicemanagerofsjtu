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
    
    def backup(self,id):
        pass
    
    def restore(self,id):
        pass

    def Touch_Reconfigure():
        """
        static method:

        tell system to detect hardware changes in the next boot
        by executing 'touch /reconfigure'
        
        warning: you may need root permission to execute it,
        check the return value to see whether it succeed.
        """
        return os.system( 'touch /reconfigure' )
    
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
        self.dev_subpath = os.popen('isainfo -k').readlines()[0][:-1]
        self.dev_path = os.popen('arch -k').readlines()[0][:-1]            

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
        dirlist = ['/kernel/drv','/usr/kernel/drv','/platform/'+self.dev_path+'/kernel/drv','']
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
        if self.dev_subpath:
            self.path = dirlist[1]+'/'+self.dev_subpath+'/'
        else:
            self.path = dirlist[1]+'/'

    def getShortPath(self):
        if self.dev_subpath:
            return 'drv/'+self.dev_subpath+'/'+self.drvname
        else:
            return 'drv/'+self.drvname
        
    def info(self):
        dict = BaseDriver.info(self)
        dict['short path'] = self.getShortPath()
        dict['full path'] = self.getFullPath()
        dict['file exists?'] = self.IsExist()
        return dict

class Driver(LocatedDriver):
    def __init__( self, drvname ):
        LocatedDriver.__init__(self,drvname);

    def dbg_Reload_Module(self, verbose = True):
        """
            Unload old modules, then reload it
            return value: 0 for succeed, anything else for failed
            Exception: None
        """
        if verbose:
            print 'reload module: ',self.getFullPath()
        try:
            ret = self.Unload_Module(verbose)
        except:
            ret = -1
        if ret != 0:
            if verbose:
                print 'Cannot unload old module :',self.drvname
            return -1

        try:
            ret = self.Load_Module(verbose)
        except:
            ret = -1
        if ret != 0:
            if vebose:
                print 'Cannot load module :', self.drvname
            return -1

        return 0

    def dbg_Load_Module(self, verbose = True):
        """
            Load modules
            return value: 0 for succeed, anything else for failed
            Exception: None
        """
        if verbose:
            print "load module:", self.drvname
        path = self.getShortPath()
        if not path:
            print 'Module ',self.drvname,' not found'
            return -1
        
        ret = os.system( 'modload -p ' + path )
        return ret
    
    def dbg_Unload_Module(self, verbose = True):
        """
            Unload modules
            return value: 0 for succeed, anything else for failed
            Exception: None
        """
        if verbose:
            print "unload module:", self.drvname
        try:
            mid = self.getId()
        except:
            mid = None # module not found?
        if mid == None:
            print 'Module ',self.drvname,' not loaded'
            return -1
        
        ret = os.system( 'modunload -i ' + str( mid ) )
        return ret

    def backup( self, id ):
        " use tar to backup the drv directory"
        pass

    def restore( self, id ):
        " use tar to restore the drv directory"
        pass

    def list_backup( self ):
        " list all backups "
        pass

    def info(self):
        dict = LocatedDriver.info(self)
        try:
            mid = self.getId()
            kinfo = getModuleInfo(mid)
            for key in kinfo.keys():
                dict[key] = kinfo[key]
        except:
            pass #currently not loaded in kernel
        return dict
    
    def getId(self):
        """
        invoke 'c_api.modulec.getModuleId'
        """
        return getModuleId(self.drvname)

    def install(self, args, verbose = True):
        """
            invoke add_drv to install drivers.
            args: 'add_drv' arguments except for driver name
            return value: 0 for succeed, anything else for failed
            Exception: None
        """
        if verbose:
            print 'install driver: ',self.drvname
        if self.dev_subpath:
            path = '/usr/kernel/drv/'+self.dev_subpath+'/'
        else:
            path = '/usr/kernel/drv/'
        
        print 'Follow these steps:'
        print 'copy device driver binary into ',path
        print 'copy device driver configures *.conf into ','/usr/kernel/drv'
        
        #pause()
        ret = os.system( 'add_drv ' + args + ' ' + self.drvname)
        #WARNING: add_drv does not support STREAM devices according to (816-4855.pdf)
        #reference to sad, autopush
        
        if ret == 0:
            BaseDriver.Touch_Reconfigure()
            print 'changes may take effect in the next reboot'
        else:
            print 'Cannot install module :',self.drvname

        return ret

    def uninstall(self, verbose = True):
        """
            invoke rem_drv to remove drivers.
            return value: 0 for succeed, anything else for failed
            Exception: None
        """
        if verbose:
            print 'uninstall driver: ',self.drvname

        ret = os.system( 'rem_drv ' + self.drvname )

        if ret == 0:
            BaseDriver.Touch_Reconfigure()
            print 'changes may take effect in the next reboot'
        else:
            print 'Cannot remove module :',self.drvname
        
        return ret
    
    def Install( self, args, verbose = True):
        """
        We can use pkg install / pkgadd to install drivers,
        or use shell command, as written in Solaris document 819-7057.pdf
        """
        if args:
            self.Install_Pkg( verbose, args )
        else:
            self.Install_Search( verbose )

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
        pass

    def Uninstall( self, args, verbose = True):
        if args:
            self.Uninstall_Pkg( verbose, args )
        else:
            self.Uninstall_Search( verbose )

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

def usage():
    print "Usage: python2.6 drv.py {install | uninstall} drvname {-q | -v}"
    print "                        info drvname"

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'install':
            Driver( sys.argv[2] ).Install( '',( sys.argv[3] == '-v' ))
        if sys.argv[1] == 'uninstall':
            Driver( sys.argv[2] ).Uninstall( '',( sys.argv[3] == '-v' ) )
        if sys.argv[1] == 'info':
            print Driver( sys.argv[2] ).info()
        else:
            usage()
    except IndexError:
        usage()

"""
Device Driver Manager

Tested methods:
[info] usage: drv.py info sppp

Implementing methods:
[install] drv.py install sppp -v | -q
[uninstall] drv.py uninstall sppp -v | -q
[backup]
[restore]
"""
