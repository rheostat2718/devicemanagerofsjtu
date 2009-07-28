#!/bin/python2.6
#check if hardware changes, and print the changed hardware into stdout
def daemon():
    import time
    import os
    import string
    oldconf = '/tmp/conf.old'
    newconf = '/tmp/conf.new'
    diffconf = '/tmp/conf.diff'
    os.system('rm '+oldconf)
    while True:
        time.sleep(1)
        os.system('prtconf > '+newconf)
        diffs = os.system('diff -Nn '+oldconf+' '+newconf+' >'+diffconf) >> 8
        if diffs == 1:
            f = open(diffconf,'r')
            p = f.readline().split()
            w = p[0].strip()
            try:
                k = string.atoi(w[1:])
                l = string.atoi(p[1])
            except:
                continue
            if w[0] == 'd':
                f1 = open(oldconf,'r')
            elif w[0] == 'a':
                f1 = open(newconf,'r')
            lines = f1.readlines()
            i = 0
            while i<l:
                print lines[k+i]
                i+=1
            f1.close()
#           elif w[0] == 'c': checkmodule
            f.close()
        os.system('mv '+newconf+' '+oldconf)
        #ch = raw_input('Press enter ...')

if __name__=='__main__':
    daemon()
