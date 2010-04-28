import os,sys

def getlist1():
    text = os.popen('pkg search -lr drv').readlines()
    l = []
    for line in text:
        line = line.strip().split()[-1]
        line = line.split('@')[0][5:]
        l.append(line)
    l1 = []
    for item in l:
        if not item in l1:
            l1.append(item)
    l1.sort()
    f = open('pkgdev.info2','w')
    for p in l1:
        f.write(p+'\n')
    f.close()
    return l1

def getline4(text):
    l = {}
    for p in text:
        u = os.popen('pkg contents -r -t file '+p+' | grep "kernel\/drv"').readlines()
        for line in u:
            line = line[:-1].split('/')[-1]
            if line.find('.') != -1:
                continue
            l[line] = p
    f = open('pkgdev.list2','w')
    for key in l.keys():
        value = l[key]
        print key,value
        f.write(key+' '+value+'\n')
    f.close()        
    return l
if __name__=='__main__':
    q = getlist1()
    getline4(q)
    
