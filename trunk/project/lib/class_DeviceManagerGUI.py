'''this file is the definition of GUI'''

import dbus
import pygtk
pygtk.require("2.0")
import gtk

from class_DeviceManager import *
from class_Device import *
from GUIcommon import KeyAndValue
from DrvFrame import *
from class_CommonDevice import *

class DeviceManagerGUI(gtk.Window):
    def __init__(self, manager):
        self.manager=manager

        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_title("Device Manager v0.3")
        self.connect("delete_event", self.delete_event)
        self.device_tree=DeviceTree(manager.getDeviceObj("root"), self)
        self.device_common=CommonDeviceList(manager.getDeviceObj("root"), self)
        #self.top.add(self.device_tree.getFrame())
        #self.top.set_size_request(300, 400)
        #self.top.show_all()

        #self.top2=gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.top2.set_title('Note')
        self.notebook=DeviceNote()
        self.notebookleft=DeviceNoteLeft(self.device_common, self.device_tree)
        #self.top2.add(self.notebook)
        #self.top2.show_all()

        self.table=gtk.Table(1,2)
        #self.table.attach(self.device_tree,0,1,0,1)
        self.table.attach(self.notebookleft,0,1,0,1)
        self.table.attach(self.notebook,1,2,0,1)

        self.add(self.table)
        self.set_size_request(800, 400)
        self.show_all()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()

    def update(self):
        self.device_tree.make_view()
        self.updateNote(self)

    def updateNote(self, device=None):
        self.notebook.update(device)


    def loop(self):
        pass

class DeviceBriefTable(KeyAndValue):
    def __init__(self, device):
        self.info={}
        try:
            self.info['vendor']=device.getVendor()
        except:
            self.info['vendor']='unknown'
        try:
            self.info['device']=device.getProduct()
        except:
            self.info['device']='unknown'
        try:
            self.info['type']=device.getType()
        except:
            self.info['type']='unknown'
        try:
            self.info['udi']=device.getUDI()
        except:
            self.info['udi']='unknown'
        KeyAndValue.__init__(self, self.info)




class DeviceDetailTable(KeyAndValue):
    def __init__(self, device):
        self.info=device.getProperties()
        KeyAndValue.__init__(self, self.info)



class DeviceTree(gtk.ScrolledWindow):
    def __init__(self, root, gui):
        self.gui=gui
        self.root=root
        gtk.ScrolledWindow.__init__(self)
        self.set_border_width(10)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.make_view()

    def make_view(self):
        try:
            self.tree_store.destroy()
            self.tree_view.destroy()
        except:
            pass

        self.make_tree()
        self.tree_view=gtk.TreeView(self.tree_store)

        self.tv_column=gtk.TreeViewColumn('Devices')
        self.tree_view.append_column(self.tv_column)

        self.cell=gtk.CellRendererText()
        self.tv_column.pack_start(self.cell, True)
        self.tv_column.add_attribute(self.cell, 'text', 0)

        self.tree_view.set_search_column(0)
        self.tv_column.set_sort_column_id(0)

        self.tree_view.set_reorderable(True)
        self.tree_view.expand_all()
        self.tree_view.connect("cursor_changed", self.selectedCallback)

        self.add_with_viewport(self.tree_view)
        self.set_size_request(300,400)

    def selectedCallback(self, tree):
        selection=self.tree_view.get_selection()
        (model, itr) = selection.get_selected()
        device=self.tree_store.get_value(itr,1)
        #DeviceDetailTable(self.gui.manager.getDeviceObj(device))
        self.gui.updateNote(self.gui.manager.getDeviceObj(device))

    def make_tree(self):
        self.tree_store=gtk.TreeStore(str, str)
        itr=self.tree_store.append(None, [self.root.getProduct(), self.root.getUDI()])
        self.append_device(itr, self.root)

    def append_device(self, parent, device):
        for child in device.getChildren():
            itr=self.tree_store.append(parent, [child.getProduct(), child.getUDI()])
            if child.hasChildren():
                self.append_device(itr, child)

class DeviceNoteLeft(gtk.Notebook):
    def __init__(self, device_common, device_tree):
        gtk.Notebook.__init__(self)
        self.set_tab_pos(gtk.POS_TOP)

        #common
        label=gtk.Label("Common")
        self.table0=gtk.Table(1,1,False)
        self.table0.attach(device_common,0,1,0,1)
        self.append_page(self.table0, label)

        #device tree
        label=gtk.Label("Device Tree")
        self.table1=gtk.Table(1,1,False)
        self.table1.attach(device_tree,0,1,0,1)
        self.append_page(self.table1, label)

        self.set_size_request(300,400)

class DeviceNote(gtk.Notebook):
    def __init__(self):
        gtk.Notebook.__init__(self)
        self.set_tab_pos(gtk.POS_TOP)

        #brief
        label=gtk.Label("Brief")
        self.table0=gtk.Table(1,1,False)
        self.append_page(self.table0, label)

        #detail
        label=gtk.Label("Detail")
        self.table1=gtk.Table(1,1,False)
        self.append_page(self.table1, label)

        #drive info
        label=gtk.Label("Driver")
        self.table2=gtk.Table(1,1,False)
        self.append_page(self.table2, label)

        self.device=None

        self.connect("switch-page", self.pageCallback)
        self.set_size_request(400,400)

    def pageCallback(self, page, pagenum, par):
        if self.device!=None:
            self.update(self.device)

    def update(self, device):
        if device==None:
            return 0;
        self.device=device

        try:
            self.brief.destroy()
        except:
            pass

        try:
            self.detail.destroy()
        except:
            pass

        self.brief=DeviceBriefTable(device)
        self.detail=DeviceDetailTable(device)
        self.driver=DriverInfoFrame(device.getDriver())
        self.table0.attach(self.brief,0,1,0,1)
        self.table1.attach(self.detail,0,1,0,1)
        self.table2.attach(self.driver,0,1,0,1)
        self.brief.show()
        self.detail.show()
        self.driver.show()
        self.table0.show()
        self.table1.show()
        self.table2.show()




