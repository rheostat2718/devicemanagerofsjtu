from Tkinter import *
import string
#import drv

class DriverInfoGUI(Frame):
    def __init__(self,parent = None,**config):
        self.bg = 'white'
        self.fg = 'blue'
        Frame.__init__(self,parent,config)
        self.labels = []
        self.config(bg = self.bg)
        self.config(bd = 1)
        Label(self,text = 'KEY : VALUE',fg=self.fg, bg=self.bg).pack(side = TOP,anchor=N)
    def packself(self):
        self.pack(expand = YES,fill = BOTH,ipadx = 1,ipady = 1)
    def run(self):
        self.mainloop()
    def cleanupLabel(self):
        for label in self.labels:
            label.destroy()
        self.labels = []
    def addLabelItem(self,indent,key,value):
        if (type(value) == type(str())) | (type(value) == type(int())) | (type(value) == type(float())):
            l = Label(self,text = str(key)+' : '+indent+str(value),fg=self.fg,bg=self.bg)
            self.labels.append(l)
            l.pack(side=TOP,anchor=N)
        elif (type(value)== type(list())):
            l = Label(self,text = str(key)+' :',fg=self.fg,bg=self.bg)
            self.labels.append(l)
            l.pack(side=TOP,anchor=N)
            for minorvalue in value:
                self.addLabelItem(indent+'|   ','',minorvalue)
        elif (type(value)== type(dict())):
            l = Label(self,text = str(key)+' :',fg=self.fg,bg=self.bg)
            self.labels.append(l)
            l.pack(side=TOP,anchor=N)
            minorkeys = value.keys()
            minorkeys.sort()
            for minorkey in minorkeys:
                self.addLabelItem(indent+'|   ',minorkey,value[minorkey])
        else:
            print type(value)
            
    def reloadInfo(self,driver = None):
#        if not (driver is drv.Driver):
#            return
#        info = driver.getInfo()
        info = {'name':'aaa','size':66,'prop':{'a':'asdf','b':'asdf'},'more':['a','b','c']}
# test only
        self.cleanupLabel()
        keys = info.keys()
        keys.sort()
        for key in keys:
            self.addLabelItem('',key,info[key])
            
if __name__=='__main__':
    g = DriverInfoGUI()
    g.packself()
    g.reloadInfo()
    g.run()

"""
TODO:
0 - anyone could make it beautiful?  ^_^||
1 - seperate it into 2 column, e.g no annoying ':'
2 - add special key to show up first, e.g 'name','size'...
3 - add sort | reverse sort | special first order
BUGFIX:
4 - find unknown type... also maybe type itself...
"""