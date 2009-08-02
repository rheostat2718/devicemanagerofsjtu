#!/bin/env python

# This script should be run under root priviledge

import os
import sys
uname_i = os.popen('uname -i').readline()[:-1]
uname_m = os.popen('uname -m').readline()[:-1]
uname_p = os.popen('uname -p').readline()[:-1]
#TODO: test uname_p
if uname_p.find("amd64") != -1:
    subdir = 'amd64/'
elif uname_p.find("sparcv9") != -1:
    subdir = 'sparcv9/'
else:
    subdir = ''
USR_KERNEL_DRV = '/usr/kernel/drv'
KERNEL_DRV = '/kernel/drv'
PLATFORM_KERNEL_DRV_I = '/platform/'+uname_i+'/kernel/drv'
PLATFORM_KERNEL_DRV_M = '/platform/'+uname_m+'/kernel/drv'

# Find driver's location by its name, also return whether its configure file location
def findDrvConf(drivername):
#    global uname_i,uname_m,subdir,USR_KERNEL_DRV,KERNEL_DRV,PLATFORM_KERNEL_DRV_I,PLATFORM_KERNEL_DRV_M
    ret = []
    dirlist = [KERNEL_DRV,USR_KERNEL_DRV,PLATFORM_KERNEL_DRV_I]
    if uname_i != uname_m:
        dirlist.append(PLATFORM_KERNEL_DRV_M)
    for currdir in dirlist:
        drvname = currdir + '/' + subdir + drivername
        if os.path.isfile(drvname):
            # it is said the driver.conf is always in .../drv
            confname = currdir + '/' + drivername +'.conf'
            if os.path.isfile(confname):
                ret.append((drvname,confname))
            # TODO: find out whether we should return None or deprecate it
            # else:
            #     ret.append((drvname,None))

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

def loadModule(modname,verbose = True):
    # Remove old modules before we load new ones
    unloadModuel(modname,quiet)
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
            print "Failed"
        else:
            print "Succeed"

#TODO: rem_drv(1M) seems automatically call MODUNLOAD
#      Is this function necessary?
def unloadModule(modname,verbose = True):
    idlist = findIdByName(modname)
    if idlist == []:
        print 'Module ',modname,' not exist'
        return;
    for i in idlist:
        unloadModId(i,verbose)

def unloadModId(idno,verbose = True)
    if verbose:
        print "Unload Module Id :",i
    ret = os.system("modunload -i "+str(idno))
    if verbose:
        if ret != 0:
            print "Failed"
        else:
            print "Succeed"

#TODO: add_drv & rem_drv automatically do this by
#fopen("/reconfigure","a")
def touchReconfigure(modname):
    os.system("touch /reconfigure")

#Doc "819-7057"  
def preInstall(drvname):
    os.system("cp "+ drvname+ ' ' + USR_KERNEL_DRV + '/' + subdir)
    os.system("cp "+ drvname+ '.conf ' + USR_KERNEL_DRV + '/')
#add_drv cannot used on STREAM
#TODO: Doc "816-4855" sad autopush
    os.system("add_drv "+drvname)
if __name__=='__main__':
    print findFirstDrvConf('sd') #/kernel/drv[/amd64]
    print findFirstDrv('pm')     #/usr/kernel/drv
    print findDrvConf('cpc')     #/platform/i86pc/kernel/drv
    print findDrv('nosuchdriver')
