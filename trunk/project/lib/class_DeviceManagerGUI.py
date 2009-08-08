'''this file is the definition of GUI'''

from Tkinter import *
from tkMessageBox import *
from Tkinter import Tk, Canvas
from idlelib.TreeWidget import TreeItem, TreeNode
from class_Device import *

class DeviceManagerGUI:
    '''this class defices the GUI'''

    def __init__(cls, manager):
        '''init part'''
        cls.manager=manager
        cls.root=Tk()
        cls.tree=DeviceTree(cls.manager, cls.root)
    def loop(cls):
        cls.root.mainloop()

class DeviceTree(Frame):
    def __init__(cls, manager, parent=None):
        Frame.__init__(cls,parent)
        cls.pack()
        cls.canvas=Canvas(cls)
        cls.canvas.config(bg='white')
        cls.canvas.pack()
        item=DeviceTreeItem(manager.getDeviceObj("root"), manager)
        cls.root=TreeNode(cls.canvas, None, item)
        print '!!!'
        cls.root.update()

class DeviceTreeItem(TreeItem):
    def __init__(cls, device, manager):
        print device
        cls.manager=manager
        cls.name=device.getProduct()
        cls.udi=device.getUDI()
        cls.children=[]
        children=device.getChildren()
        for child in children:
            cls.children.append(child.getUDI())
            print child.getUDI()

    def GetText(cls):
        return cls.name
    def IsExpandable(cls):
        return not cls.children==[]
    def GetSubList(cls):
        parent=self.udi
        print parent
        children=[]
        prelist=[DeviceTreeItem(child) for child in self.manager.getDeviceObj(cls.children)]
        print prelist #
        return prelist
