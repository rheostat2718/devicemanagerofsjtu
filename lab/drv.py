#!/bin/env python2.6
import os
import sys
from c_api.modulec import *

class Driver():
    def __init__( self, drvname ):
        self.drvname = drvname #设备名/驱动名
        try:
            self.defaultdrvpath, self.defaultconfpath = getFirstDriverPathConf()
        except:
            self.defaultdrvpath = '' #驱动程序路径
            self.defaultconfpath = '' #驱动程序配置路径

    def dbg_setDefaultDrvPath( self, path ):
        self.defaultdrvpath = path

    def dbg_setDefaultConfPath( self, path ):
        self.defaultconfpath = path

    def isInstalled( self ): #驱动是否安装
        return ( self.getInfo()['INSTALLED'] != 0 )

    def isLoaded( self ): #驱动是否加载
        return ( self.getInfo()['LOADED'] != 0 )

    def getAllDriverPath( self ): #返回所有相关驱动程序的路径
        ret = []
        for ( a, b ) in findDrvConf( self.drvname ):
            ret.append( a )
        return ret

    def getFirstDriverConfPath( self ): #返回默认的驱动程序与配置
        return self.getAllDriverConfPath()[0]

    def getFirstDriverPath( self ): #返回默认的驱动程序
        return self.getAllDriverPath()[0]

    def getAllDriverConfPath( self ): #获得所有相关驱动程序与配置的路径
        import module
        #Having more than 2 subdir is completely possible, e.g. some on 32b system and others on 64b system
        subdirlist = []
        mapdict = {'amd64':'amd64', 'sparcv9':'sparcv9', 'i386':'.'}
        for name in os.popen( 'isainfo -k' ).readline().split():
            subdirlist.append( mapdict[name] )
        ret = []
        for currdir in getModPath().split:
            for subdir in subdirlist:
                drvname = currdir + os.path.sep + 'drv' + os.path.sep + subdir + os.path.sep + self.drvname
                if os.path.isfile( drvname ):
                    # driver.conf 始终在 .../drv 下
                    confname = currdir + os.path.sep + 'drv' + os.path.sep + self.drvname + '.conf'
                    if os.path.isfile( confname ):
                        ret.append( ( drvname, confname ) )
#FIXME: I don't know whether should return None or deprecate it
                    else:
                        ret.append( ( drvname, None ) )
        return ret

    def dbg_loadModule( self, verbose = True ): #手动加载模块
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

    def dbg_unloadModule( self, verbose = True ): #手动卸载模块
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

    def dbg_touchReconf(): #重新启动后检测硬件变化？
        """
        just tell the system to find new hardware in the next boot,
        execute it to setup it manually
        """
        return os.system( 'touch /reconfigure' )

    def Backup( self ): #备份
        return

    def Restore( self ): #还原
        return

    def isBackup( self ): #是否有备份
        return False

    def getInfo( self ): #获取模块的信息
        id = self.getId()
        if id == None:
            return
        try:
            return getModuleInfo( id )
        except:
            pass

    def getId( self ): #获得模块的id，未加载则返回None
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

    def Install_Pkg( self, verbose, pkgname ): #安装.pkg文件
        if os.path.isfile( pkgname ):
            if verbose:
                print 'Install from ', pkgname
                opt = ''
            else:
                opt = ' 2>/dev/null'
#TODO: find out the cmd
#            ret = os.system('pfexec pkgadd '+pkgname+opt)
            return ret
        else:
            print 'Cannot find ', pkgname
            return

    def Install_Cpy( self, verbose, args ): #将args中文件复制到驱动目录
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
        import package
        driverPkg = Package( self.drvname, search = True, verbose )
        if driverPkg.name == None:
            if verbose:
                print 'Cannot find related package'
            return
        try:
            return driverPkg.Install( verbose )
        except:
            pass

    def Update( self ):
        return

    def Uninstall( self, removeFromPackage = True, verbose = True, arg = None ):
        try:
            if removeFromPackage:
                if arg != None:
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
'''
    if verbose:
        print "Remove Module ", drvname
    ret = os.system( "rem_drv -C " + drvname )
    if ret < 0:
        if verbose:
            print 'Operation failed!'
        return
    ( path, filename ) = os.path.split( drvname )
    if removeFromPackage:
        import pkg
        pkgname = pkg.findPkg( filename, verbose )
        if pkgname == None:
            print 'No package found'
            return
        else:
            print 'Package ', pkgname, ' found, now uninstalling...'
        ret = pkg.uninstallPackage( pkgname , verbose )
        if ret < 0:
            return
        else:
            return ret
#    else:
#        os.system( " rm -f drvname" )
#        os.system( ' rm -f ' + drvname + '.conf' )
'''

if __name__ == '__main__':
    if len( sys.argv ) < 2:
        print "Usage: python drv.py [install | uninstall | info] drvname [-q | -v]"
    else:
        if sys.argv[1] == 'install':
            installDrv( sys.argv[2], True, ( sys.argv[3] == '-v' ) )
        if sys.argv[1] == 'uninstall':
            uninstallDrv( sys.argv[2], True, ( sys.argv[3] == '-v' ) )
        if sys.argv[1] == 'info':
            print( Driver( sys.argv[2] ).getInfo() )
