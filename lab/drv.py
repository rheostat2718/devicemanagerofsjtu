#!/bin/env python
import os
import sys

# Find driver's location by its name, also return whether its configure file location
def findDrvConf(drivername):
    uname_i = os.popen('uname -i').readline()[:-1]
    uname_m = os.popen('uname -m').readline()[:-1]
    #TODO: find out platform information SPARC/AMD64/32
    #eg, subdir = 'amd64'
    subdir = ''
    ret = []

    KERNEL_DRV = '/kernel/drv'
    USR_KERNEL_DRV = '/usr/kernel/drv'
    PLATFORM_KERNEL_DRV_I = '/platform/'+uname_i+'/kernel/drv'
    PLATFORM_KERNEL_DRV_M = '/platform/'+uname_m+'/kernel/drv'
    dirlist = [KERNEL_DRV,USR_KERNEL_DRV,PLATFORM_KERNEL_DRV_I]
    if uname_i != uname_m:
        dirlist.append(PLATFORM_KERNEL_DRV_M)
    for currdir in dirlist:
        #search for driver itself
        if subdir != '':
            drvname = currdir + '/' + subdir + '/' + drivername
        else:
            drvname = currdir + '/' + drivername
        if os.path.isfile(drvname):
            # it is said the driver.conf is always in .../drv
            confname = currdir + '/' + drivername +'.conf'
            if os.path.isfile(confname):
                ret.append((drvname,confname))
            # TODO: find out whether should we return None
            else:
                ret.append((drvname,None))

    return ret

# return the first result in the list
def findFirstDrvConf(drivername):
    l = findDrvConf(drivername)
    if l == []:
        return None
    else:
        return l[0]
    
# just return driver path
def findDrv(drivername):
    ret = []
    for tup in findDrvConf(drivername):
        ret.append(tup[0])
    return ret

def findFirstDrv(drivername):
    l = findDrvConf(drivername)
    if l == []:
        return None
    else:
        return l[0][0]

def loadModule(modname,quiet):
    #it is said we should remove old ones
    #TODO: unloadModule
    #unloadModuel(modname,True)
    opt = ''
    if (not quiet):
        opt = ' 2>/dev/null'
    drvlist = findDrv(modname)
    if (not quiet) & drvlist == []:
        print "Cannot find module :",modname
        
    for drv in drvlist:
        if (not quiet):
            print "Load Module :",drv
        ret = os.system('modinst '+drv+opt)
        if ret != 0 & (not quiet):
            print "Failed!"
        else:
            print "Succeed!"
    
if __name__=='__main__':
    print findFirstDrvConf('sd') #/kernel/drv[/amd64]
    print findFirstDrv('pm')     #/usr/kernel/drv
    print findDrvConf('cpc')     #/platform/i86pc/kernel/drv
    print findDrv('nosuchdriver')
