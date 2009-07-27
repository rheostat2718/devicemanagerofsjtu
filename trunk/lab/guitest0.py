#!/bin/python2.6
from Tkinter import *
import sys
def createWindow():
    root = Tk()
    root.title('Device manager')
    Button(root,text='detail',command=None).pack()
    Button(root,text='quit',command=root.destroy).pack()
    return root
if __name__=='__main__':
    root = createWindow()
    root.mainloop()
