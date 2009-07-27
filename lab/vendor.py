import os
#load local data or update it from internet (if possible)
#and create a dictionary
urlname = 'http://www.pcidatabase.com/reports.php?type=csv'
updatename = 'update.dat'
dataname = 'vendor.dat'
def createDict():
    global urlname,updatename,dataname
    import urllib
    import string
    d = {}
    s = dataname
    try:
        f=urllib.urlopen(urlname)
        g=open(updatename,'w')
        for line in f.readlines():
            #remove unnecessary character "
            line = line.replace('"','')
            g.write(line)
        g.close()
        ret = os.system('cp '+updatename+' '+dataname)
        if ret != 0:
            s = updatename
    except:
        pass
    print 'Loading %s' %s
    try:
        f=open(s,'r')
    except:
        return d
    for line in f.readlines():
        l = line.split(',')
        try:
            vid = string.atol(l[0],16)
            did = string.atol(l[1],16)
            d[(vid,did)]=(l[2],l[3],l[4])
        except:
            pass
    f.close()
    print 'Dictionary created'
    return d

#search for an specific item by vendor_id & driver_id
def searchid(dic,vendor_id,driver_id):
    import string
    try:
#        if (vendor_id is str) & (driver_id is str):
            #easy to transfer hex number
        vid = string.atoi(vendor_id,16)
        did = string.atoi(driver_id,16)
        print "v%d d%d"%(vid,did)
        return dic[(vid,did)]
#        else:
#            return dic[(vendor_id,driver_id)]
    except:
        return ('Unknown','Unknown','Unknown')
if __name__=='__main__':
    dic = createDict()
    while True:
        vid = raw_input("Input vid :")
        did = raw_input("Input did :")
        if (vid == 'q') | (did == 'q'):
            break
        (a,b,c)=searchid(dic,vid,did)
        print 'a = %s'%a
        print 'b = %s'%b
        print 'c = %s'%c
