'''this file is the definition of GUI'''

import dbus
import pygtk
pygtk.require("2.0")
import gtk

from class_DeviceManager import *
from class_Device import *

class DeviceManagerGUI:
    def __init__(self, manager):
        self.manager=manager

        self.top=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.top.set_title("Device Manager v0.1")
        self.top.connect("delete_event", self.delete_event)
        self.device_tree=DeviceTree(manager.getDeviceObj("root"), self)
        self.top.add(self.device_tree.getFrame())
        self.top.set_size_request(300, 400)
        self.top.show_all()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()

    def loop(self):
        pass

class DeviceDetailTable:
    def __init__(self, device):
        self.device=device
        self.top=gtk.Dialog(gtk.WINDOW_TOPLEVEL)
        self.top.set_title("detail")
        self.update(device)

        self.scrolled_window=gtk.ScrolledWindow()
        self.scrolled_window.set_border_width(10)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.scrolled_window.add_with_viewport(self.table)

        self.top.add(self.scrolled_window)
        self.top.set_size_request(300, 400)
        self.top.show_all()

    def update(self, device):
        prop=device.getProperties()
        length=len(prop)
        self.table=gtk.Table(length+1,2)
        table=self.table
        text=gtk.Label('key')
        table.attach(text,0,1,0,1)
        text.show()
        text=gtk.Label('value')
        table.attach(text,1,2,0,1)
        text.show()

        count=1
        for (key,value) in prop.items():
            text=gtk.Label(key)
            table.attach(text,0,1,count,count+1)
            text.show()
            text=gtk.Label(value)
            table.attach(text,1,2,count,count+1)
            text.show()
            count+=1

        table.show()

class DeviceTree:
    def __init__(self, root, gui):
        self.gui=gui

        self.scrolled_window=gtk.ScrolledWindow()
        self.scrolled_window.set_border_width(10)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        self.make_tree(root)
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

        self.scrolled_window.add_with_viewport(self.tree_view)

        self.tree_view.connect("cursor_changed", self.selectedCallback)
        #self.selection=self.tree_view.get_selection()
        #self.selection.set_select_function(self.selectedCallback)


    def selectedCallback(self, p1):
        selection=self.tree_view.get_selection()
        (store, itr)=selection.get_selected()
        try:
            print self.tree_store.get_value(itr,0)
        except:
            pass
        finally:
            print '!'
        #detail=DeviceDetailTable(self.gui.manager.getDeviceObj(device))

    def getFrame(self):
        return self.scrolled_window

    def make_tree(self, root):
        self.tree_store=gtk.TreeStore(str)
        itr=self.tree_store.append(None, [root.getProduct()])
        self.append_device(itr, root)

    def append_device(self, parent, device):
        for child in device.getChildren():
            itr=self.tree_store.append(parent, [child.getProduct()])
            if child.hasChildren():
                self.append_device(itr, child)

