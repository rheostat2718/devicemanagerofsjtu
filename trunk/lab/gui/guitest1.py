#!/bin/python2.6
from Tkinter import *
def loaddata():
    import os
    lines = os.popen('./exp1').readlines()
    text=''
    for line in lines:
        text+=line
    return text
def test():
    root=Tk()
    root.title('Test')
    l=loaddata()
    t=Listbox(root,text=loaddata())
    t.pack(expand=YES,fill=BOTH)
    root.mainloop()

if __name__=='__main__':
    test()
