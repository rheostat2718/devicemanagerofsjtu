import os, sys

"""
execute 'psrinfo -p | -v | -pv'
collect processor status & name & virtual processors

usage : read_psrinfo()
return type : a list of processors information, each item is a key-value dict
keys are:
pid / status / stime / name / name2 / other / virtual processor count / virtual processor
"""

def read_psrinfo():
    list = []
    output = os.popen('psrinfo -p').readlines()
    if not output:
        return list
    try:
        count =int(output[0][:-1])
    except ValueError:
        return list
    for i in range(count):
        output =os.popen('psrinfo -v '+str(i)).readlines()
        dict = {'pid':i}
        if output:
            line = output[1]
            try:
                stat,stime = line.split('since') # status, since when
                dict['status']=stat.strip() #online spare off-line faulted  powered off non-interruptible
                dict['stime']=stime.strip()[:-1]
            except ValueError:
                pass
            try:
                line = output[3].strip()
                if line[:4]=='and ':
                    line = line[4:]
                dict['other']=line
            except IndexError:
                pass
        output = os.popen('psrinfo -pv '+str(i)).readlines()
        if output:
            #unresolved keys for cpu-name
            dict['name'] = output[1].strip()
            dict['name2'] = output[2].strip()
            
            try:
                line = output[0].split('has ')[1]
                sets = line.split()
                vnum = int(sets[0]) #virtual processor numbers
                dict['virtual processor count']=vnum
                vsets = sets[-1][1:-1].split(',') #sets[-1] = (1,2,3,...)
                dict['virtual processor'] = vsets
            except IndexError,ValueError:
                pass
        list.append(dict)
    return list

if __name__ == '__main__':
    for item in read_psrinfo():
        print item