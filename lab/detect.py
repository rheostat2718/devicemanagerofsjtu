#!/bin/python2.6
#it seems a simple shell script may fulfill the task
#but we may need some post processing ... later
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
            if w[0] == 'd':
                k = string.atoi(w[1:])
                l = string.atoi(p[1]
                f1 = open(oldconf,'r')
                lines = f1.readlines()
                line = lines[k]
                f1.close()
                #checkmodule
            elif w[0] == 'a':
                #checkmodule
            elif w[0] == 'c':
                #checkmodule
            f.close()
        os.system('mv '+newconf+' '+oldconf)
        #ch = raw_input('Press enter ...')

if __name__=='__main__':
    daemon()
