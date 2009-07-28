#!/bin/python2.6
import os
#load local data or update it from internet (if possible)
#and create a dictionary
urlname = 'http://www.pcidatabase.com/reports.php?type=csv'
updatename = 'update.dat'
dataname = 'vendor.dat'

#update data from network
#use signal.alarm to stop slow connection
def updateDict():
    global urlname,updatename,dataname
    import urllib
    import signal
    s = dataname
    try:
        def onSignal():
            raise IOError()
        signal.signal(signal.SIGALRM,onSignal)
        signal.alarm(10)
        f=urllib.urlopen(urlname)
        g=open(updatename,'w')
        for line in f.readlines():
            #remove unnecessary character "
            line = line.replace('"','')
            g.write(line)
        g.close()
        signal.signal(signal.SIGALRM,signal.SIG_IGN)
        f.close()
        if os.path.exists(dataname) & os.path.isdir(dataname):
            s = updatename
        else:
            ret = os.system('mv '+updatename+' '+dataname)
            if ret != 0:
                s = updatename
    except:
        pass
    return createDict(s)

#create dict from file    
def createDict(filename):
    print "Create directory from %s"%filename
    import string
    d = {}
    try:
        f=open(filename,'r')
    except:
        return d
    for line in f.readlines():
        l = line.split(',')
        try:
            vid = string.atol(l[0],16)
            did = string.atol(l[1],16)
            d[(vid,did)]=(l[2],l[3],l[4][:-1])
        except:
            pass
    f.close()
    return d

#search for an specific item by vendor_id & driver_id
def searchid(dic,vendor_id,driver_id):
    import string
    try:
#        if (vendor_id is str) & (driver_id is str):
            #easy to transfer hex number
        vid = string.atoi(vendor_id,16)
        did = string.atoi(driver_id,16)
#        print "v%d d%d"%(vid,did)
        return dic[(vid,did)]
#        else:
#            return dic[(vendor_id,driver_id)]
    except:
        return ('Unknown','Unknown','Unknown')
    
#just put three driver string into one...
def longName(str1,str2,str3):
    if (str1 == 'Unknown') & (str2 == 'Unknown') & (str3 == 'Unknown'):
        return 'Unknown'
    s = str1+str2+str3
    s = s.replace('  ',' ')
    if s[0] == ' ':
        if s[-1] == ' ':
            return s[1:-1]
        else:
            return s[1:]
    else:
        if s[-1] == ' ':
            return s[:-1]
        else:
            return s

if __name__=='__main__':
    dic = updateDict()
    while True:
        vid = raw_input("Input vid :")
        did = raw_input("Input did :")
        if (vid == 'q') | (did == 'q'):
            break
        (a,b,c)=searchid(dic,vid,did)
        print "%s"%(longName(a,b,c))
