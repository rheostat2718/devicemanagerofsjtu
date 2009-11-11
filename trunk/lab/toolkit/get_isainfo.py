import os,sys

"""
execute 'isainfo -x'
collect cpu instruction sets information

usage : read_isainfo(get_isainfo()):
return type : a key-value dict as
cpu-mode : a list supported instruction sets
"""

def get_isainfo():
    return os.popen("isainfo -x").readlines()

def read_isainfo(lines):
    dict = {}
    for line in lines:
        ret = []
        try:
            name,sets = line.split(':')
            slist = sets.split()
            for item in slist:
                if item:
                    ret.append(item)
            dict[name] = ret
        except ValueError:
            continue
    return dict

if __name__=='__main__':
    output = get_isainfo()
    if not output:
        output = open('isainfo.txt').readlines()
    print read_isainfo(output)