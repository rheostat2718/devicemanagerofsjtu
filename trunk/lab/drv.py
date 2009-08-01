#!/bin/env python
# find driver's absolute path & return a list of possible location
def findDrvConf(drivername):
    import os,sys,glob
    ret = []
    platform = os.popen('uname -m').readline()[:-1] # or obtain it from struct utsname in C?
    KERNEL_DRV = '/kernel/drv'
    USR_KERNEL_DRV = '/usr/kernel/drv'
    PLATFORM_XXX_KERNEL_DRV = '/platform/'+platform+'/kernel/drv'
#    PLATFORM_XXX_KERNEL_DRV = '/platform/*/kernel/drv'

    for currdir in [KERNEL_DRV,USR_KERNEL_DRV,PLATFORM_XXX_KERNEL_DRV]:
        #search in the directory
        drvname = currdir + '/' + drivername
        if os.path.isfile(drvname):
            confname = drvname + '.conf'
            if os.path.isfile(confname):
                ret.append((drvname,confname))
#   according to modload's script, driver with out .conf are not included
#   FIXME :
#            else:
#                ret.append((drvname,None))

    for currdir in [KERNEL_DRV,USR_KERNEL_DRV,PLATFORM_XXX_KERNEL_DRV]:
        #search in the subdirectory
        for drvname in glob.glob(currdir + '/*/'+drivername):
            confname = drvname + '.conf'
            if os.path.isfile(confname):
                ret.append((drvname,confname))
#            else:
#                ret.append((drvname,None))
                   
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
    import os,sys
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
