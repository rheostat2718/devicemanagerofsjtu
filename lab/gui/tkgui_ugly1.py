from Tkinter import *
import sys
import os

class MainGUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Device Manager')
        MainFrame(self)
        self.mainloop()

class MainFrame(Frame):
    def __init__(self,parent=None,**config):
        Frame.__init__(self,parent,**config)
        self.pack(expand=YES,fill=BOTH)
        self.make_widgets()

    def make_widgets(self):
        menu = Menu(self)
        bottom = BottomLines(self)
        left = LeftSide(self)
        right = RightSide(self)

class Menu(Frame):
    def __init__(self,parent=None,**config):
        Frame.__init__(self,parent,**config)
        self.pack(side=TOP,expand=YES,fill=X,anchor=N)
        self.config(bg='grey')
        self.make_widgets()
    def make_widgets(self):
        Label(self,text='Menu').pack(side=LEFT)
        Button(self,text='Exit',command=sys.exit).pack(side=RIGHT,anchor=E)
        
class LeftSide(Frame):
    def __init__(self,parent=None,**config):
        Frame.__init__(self,parent,**config)
        self.pack(side=LEFT,expand=YES,fill=Y,anchor=W)
        self.config(bg='#0077ff')
        self.make_widgets()
    def make_widgets(self):
        Label(self,text='Left').pack()
#        DevTree(self).pack()
#       get device tree, list here

class RightSide(Frame):
    def __init__(self,parent=None,**config):
        Frame.__init__(self,parent,**config)
        self.pack(side=RIGHT,expand=YES,fill=BOTH)
        self.config(bg='white')
        self.make_widgets()
    def make_widgets(self):
        Label(self,text='Right').pack()
#       get information

class BottomLines(Frame):
    def __init__(self,parent=None,**config):
        Frame.__init__(self,parent,**config)
        self.pack(side=BOTTOM,expand=YES,fill=X,anchor=S)
        self.config(bg='grey')
        self.make_widgets()
    def make_widgets(self):
        p = LabelFrame(self,text='Buttons | console')
        p.pack(side=TOP,expand=YES,fill=X)
        p.config(bg='white')
        Button(p,text='Exit',command=sys.exit).pack()
        Label(self,text='Status Line').pack(side=BOTTOM)
#       supply Button | status ...

if __name__=='__main__':
    MainGUI()
