from Tkinter import *
import string
#import drv

class DriverInfoGUI(Frame):
    def __init__(self,parent = None,**config):
        self.bg = 'white'
        self.fg = 'blue'
        self.titlefont = ('Helvetica',12,'normal')
        self.leftfont=('Courier',11,'bold')
        self.rightfont=('Courier',11,'normal')
        self.leftlabels = []
        self.rightlabels = []
        Frame.__init__(self,parent,config)
        self.config(bg = self.bg)
        self.config(bd = 1)
        self.left = LabelFrame(self,text='key',fg = self.fg,bg=self.bg,font=self.titlefont)
        self.left.pack(side=LEFT,expand=YES,fill=BOTH)
        self.right = LabelFrame(self,text='value',fg = self.fg,bg=self.bg,font=self.titlefont)
        self.right.pack(side=RIGHT,expand=YES,fill=BOTH)

    def packself(self):
        self.pack(expand = YES,fill = BOTH,ipadx = 1,ipady = 1)

    def run(self):
        self.mainloop()
        
    def cleanupLabel(self):
        for label in self.leftlabels:
            label.destroy()
        for label in self.rightlabels:
            label.destroy()
        self.leftlabels = []
        self.rightlabels = []
        
    def addLabelItem(self,lindent,rindent,key,value):
        if (type(value) == type(str())) | (type(value) == type(int())) | (type(value) == type(float())):
            l1 = Label(self.left,text = lindent+str(key),fg=self.fg,bg=self.bg,font=self.leftfont)
            l2 = Label(self.right,text = rindent+str(value),fg=self.fg,bg=self.bg,font=self.rightfont)
            self.leftlabels.append(l1)
            self.rightlabels.append(l2)
            l1.pack(side=TOP,anchor=NW)
            l2.pack(side=TOP,anchor=NW)
        elif (type(value)== type(list())):
            l1 = Label(self.left,text = lindent+str(key),fg=self.fg,bg=self.bg,font=self.leftfont)
            l2 = Label(self.right,text = rindent,fg=self.fg,bg=self.bg,font=self.rightfont)
            self.leftlabels.append(l1)
            self.rightlabels.append(l2)
            l1.pack(side=TOP,anchor=NW)
            l2.pack(side=TOP,anchor=NW)
            for minorvalue in value:
                self.addLabelItem(lindent+'|-',rindent+'  ','',minorvalue)
        elif (type(value)== type(dict())):
            l1 = Label(self.left,text = lindent+str(key),fg=self.fg,bg=self.bg,font=self.leftfont)
            l2 = Label(self.right,text = rindent,fg=self.fg,bg=self.bg,font=self.rightfont)
            self.leftlabels.append(l1)
            self.rightlabels.append(l2)
            l1.pack(side=TOP,anchor=NW)
            l2.pack(side=TOP,anchor=NW)
            minorkeys = value.keys()
            minorkeys.sort()
            for minorkey in minorkeys:
                self.addLabelItem(lindent+'|',rindent+'- ',minorkey,value[minorkey])
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
            self.addLabelItem('','',key,info[key])
            self.addLabelItem('','','','')
            
if __name__=='__main__':
    g = DriverInfoGUI()
    g.packself()
    g.reloadInfo()
    g.run()

"""
TODO:
1 - anyone could make it beautiful?  ^_^||
2 - add special key to show up first, e.g 'name','size'...
3 - add sort | reverse sort | special first order
5 - add scrollbar?,listbox?
BUGFIX:
4 - find unknown type... also maybe type itself...
"""