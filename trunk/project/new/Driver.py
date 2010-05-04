#!/bin/python2.6
import os
import logging
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
        dict = {'name':self.drvname} #short-name
        dict['locate.drvfile'] = self.getDrvPath()
        #dict['short path'] = self.getShortPath()
        dict['locate.conffile'] = self.getConfPath()
        dict['locate.exist_drifile'] = self.existDrv()
        dict['locate.exist_conffile'] = self.existConf()
        return dict

    def install( self ):
        logging.DEBUG( "install" + self.drvname )

    def uninstall( self ):
        logging.DEBUG( "uninstall" + self.drvname )

    def update( self ):
        logging.DEBUG( "update" + self.drvname )

    def backup( self, filename ):
        " use tar to backup the drv directory"
        #store configuration in case of data corruption during driver operation
        logging.DEBUG( "backup" + self.drvname )

    def restore( self, filename ):
        " use tar to restore the drv directory"
        #restore configuration from filename 
        logging.DEBUG( "restore" + self.drvname )

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
        self.dev_machine = os.popen( 'uname -m' ).readlines()[0][:-1]
        self.dev_process = os.popen( 'uname -p' ).readlines()[0].strip()
        subdict = {'amd64':'amd64/', 'sparcv9':'sparcv9/', 'i386':''}
        self.dev_subpath = subdict[self.dev_instset]

        #print 'dev_instset', self.dev_instset
        #print 'dev_machine', self.dev_machine
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
        dirlist = ['/kernel/drv', '/usr/kernel/drv', '/platform/' + self.dev_machine + '/kernel/drv']

        for directory in dirlist:
            if not directory:
                break

            if os.path.exists( directory + '/' + self.dev_subpath + self.drvname ):
                self.path = directory + '/' + self.dev_subpath
                self.confpath = directory + '/'
                return True

        #use a default path here:
        self.path = dirlist[1] + '/' + self.dev_subpath
        self.confpath = dirlist[1] + '/'
        return False

    def getShortPath( self ):
        return 'drv/' + self.dev_subpath + self.drvname

class Driver( BaseDriver ):
    def __init__( self, drvname ):
        BaseDriver.__init__( self, drvname );

    def info( self ):
        #driver location information
        dict = BaseDriver.info( self )
        try:
            mid = self.getModuleId()
            print mid
            kinfo = modulec.getModuleInfo( mid )
            for key in kinfo.keys():
                dict['module.' + key] = kinfo[key]
        except SystemError:
            pass #currently not loaded in kernel
        return dict

    def getModuleId( self ):
        """
        invoke 'c_api.modulec.getModuleId'
        """
        return modulec.getModuleId( self.drvname )
