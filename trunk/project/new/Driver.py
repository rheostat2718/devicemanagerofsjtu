#!/bin/python2.6
import os
import sys
#import #logging
#import logger
import c_api.modulec as modulec

class BaseDriver( object ):
    """
    Driver class which can locate driver file
    """
    def __init__( self, drvname, path = '', confpath = '' ):
        self.drvname = drvname
        self.confname = drvname + '.conf'
        self.collect_env()
        if path or confpath:
            self.manualLocate( path, confpath )
        else:
            self.locateDrvConf()

    def info( self ):
        dict = {'locate.name':self.drvname}
        dict['locate.driver_file'] = self.getDrvPath()
        dict['locate.configure_file'] = self.getConfPath()
        dict['locate.exist_drvfile'] = self.existDrv()
        dict['locate.exist_conffile'] = self.existConf()
        return dict

    def install( self ):
        pass
        #logging.debug( "install" + self.drvname )

    def uninstall( self ):
        pass
        #logging.debug( "uninstall" + self.drvname )

    def update( self ):
        pass
        #logging.debug( "update" + self.drvname )

    def backup( self, filename ):
        " use tar to backup the drv directory"
        pass
        #store configuration in case of data corruption during driver operation
        #logging.debug( "backup" + self.drvname )

    def restore( self, filename ):
        " use tar to restore the drv directory"
        pass
        #restore configuration from filename
        #logging.debug( "restore" + self.drvname )

    def list_backup( self ):
        " list all backups "
        pass

    def getDrvPath( self ):
        return self.path + self.drvname

    def getConfPath( self ):
        return self.confpath + self.confname

    def collect_env( self ):
        """
        exec some Tools to get necessary information to
        locate drivers
        """
        #"32" or "64"
        self.env_bit = os.popen( 'isainfo -b' ).readlines()[0][:2]

        self.dev_instset = os.popen( 'isainfo -k' ).readlines()[0][:-1]
        self.dev_process = os.popen( 'uname -p' ).readlines()[0].strip()
        subdict = {'amd64':'amd64/', 'sparcv9':'sparcv9/', 'i386':''}
        self.dev_subpath = subdict[self.dev_instset]

        #print 'dev_instset', self.dev_instset
        #print 'dev_process', self.dev_process
        #print 'dev_subpath', self.dev_subpath

    def existDrv( self ):
        return os.path.exists( self.getDrvPath() )

    def existConf( self ):
        return os.path.exists( self.getConfPath() )

    def manualLocate( self, path, confpath ):
        self.path = path
        self.confpath = confpath

    def locateDrvConf( self ):
        """
        Automatically find the path of device file
        find in:
        /kernel/drv /usr/kernel/drv /platform/xxxx/kernel/drv ... /  {amd64/,sparcv9/,}

        """
        dirlist = modulec.getModPath().split()
        dirlist = [dir + '/drv' for dir in dirlist]
        #dirlist = ['/kernel/drv', '/usr/kernel/drv', '/platform/' + self.dev_machine + '/kernel/drv']

        for directory in dirlist:
            if not directory:
                break

            if os.path.exists( directory + '/' + self.dev_subpath + self.drvname ):
                self.path = directory + '/' + self.dev_subpath
                self.confpath = directory + '/'
                return True

        #use a default path here:
        if dirlist:
            self.path = dirlist[0] + '/' + self.dev_subpath
            self.confpath = dirlist[0] + '/'
        else:
            self.path = ''
            self.confpath = ''
        return False

    def getShortPath( self ):
        return 'drv/' + self.dev_subpath + self.drvname

class Driver( BaseDriver ):
    def __init__( self, drvname ):
        BaseDriver.__init__( self, drvname );

    def info( self ):
        #driver location information
        dict = BaseDriver.info( self )
        mid = self.getModuleId()
        if mid != -1:
            try:
                kinfo = modulec.getModuleInfo( mid )
                for key in kinfo.keys():
                    dict['module.' + key] = kinfo[key]
            except SystemError:
                pass
        return dict

    def key_info( self ):
        dict = self.info()
        key_dict = {}
        keyword = {'locate.name':'driver', 'locate.exist_drvfile':'exist', 'module.LOADED':'load'}

        for key in keyword.keys():
            if key_dict.has_key( key ):
                key_dict[key] = dict[keyword[key]]
        return key_dict

    def getModuleId( self ):
        """
        invoke 'c_api.modulec.getModuleId'
        -1 will be returned if not found.
        """
        return modulec.getModuleId( self.drvname )

    def install( self,send, args = '', filelist = [], src = None, dst = None ):
        """
        call run_adddrv to install drivers.
        args: 'add_drv' arguments except for driver name
        return value: 0 for succeed, anything else for failed
        """
        #BaseDriver.install( self )
        #if os.geteuid() != 0:
        #    return - 1

        if not self.existDrv():
            if ( not src ) or ( not dst ) or ( not filelist ):
                return False

            for filename in filelist:
                if src[-1] != '/':
                    src = src + '/'
                srcfile = src + filename
                if dst[-1] != '/':
                    dst = dst + '/'
                dstfile = dst + filename
                ret = send( 'CMD:cp ' + srcfile + ' ' + dstfile )

        import tools
        #here args are not used
        ret = tools.run_adddrv(send, self.drvname )
        return ( ret == 0 )

    def uninstall( self, removeFile = False ):
        """
       invoke rem_drv to remove drivers.
       return value: 0 for succeed, anything else for failed
       """

        BaseDriver.uninstall( self )
        if os.geteuid() != 0:
            return - 1

        import tools
        ret = tools.run_remdrv( self.drvname, removeConfigure = removeFile )
        return ( ret == 0 )

    def load( self ):
        """
        Load modules
        return value: 0 for succeed, anything else for failed
        """
        if not self.existDrv():
            return False
        #logging.debug( "load module " + self.drvname )

        path = self.getShortPath()
        ret = os.system( 'modload -p ' + path )
        return ( ret == 0 )

    def unload( self ):
        """
        Unload modules
        return value: 0 for succeed, anything else for failed
        """
        #logging.debug( "unload module " + self.drvname )
        mid = self.getModuleId()
        if mid == -1:
            return False

        ret = os.system( 'modunload -i ' + str( mid ) )
        return ( ret == 0 )

def usage():
    print "Usage: python drv.py {install | uninstall} drvname"
    print "                        info drvname"

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'install':
            print Driver( sys.argv[2] ).install()
        elif sys.argv[1] == 'uninstall':
            print Driver( sys.argv[2] ).uninstall()
        elif sys.argv[1] == 'info':
            print Driver( sys.argv[2] ).info()
        else:
            usage()
    except IndexError:
        usage()

"""
Device Driver Manager

Tested methods:
[info] usage: Driver.py info sppp

Implementing methods:
[install] drv.py install sppp
[uninstall] drv.py uninstall sppp
"""
