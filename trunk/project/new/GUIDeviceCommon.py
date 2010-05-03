import os
import re
import gtk

from DeviceManagerGUI import *

class DeviceCommonList(gtk.ScrolledWindow):
    def __init__(self, dev_root, gui):
        gtk.ScrolledWindow.__init__(self)
        self.set_border_width(10)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        self.list={}
        self.gui=gui
        self.root=dev_root

        txt=os.popen('./all_devices')

        for line in txt.readlines():
            if len(line)>3:
                device_common=DeviceCommon(line)
                device_common.update_udi(self.find_udi(device_common.udi, self.root))
                if device_common.udi is not None:
                    self.list[device_common.name]=device_common.udi
        txt.close()

        self.make_view()

    def make_view(self):
        try:
            self.store.destroy()
            self.view.destroy()
        except:
            pass

        self.store=gtk.TreeStore(str, str)
        for dev,udi in self.list.items():
            self.store.append(None, [dev, udi])

        self.view=gtk.TreeView(self.store)
        self.column=gtk.TreeViewColumn('Devices')
        self.view.append_column(self.column)

        self.cell=gtk.CellRendererText()
        self.column.pack_start(self.cell, True)
        self.column.add_attribute(self.cell, 'text', 0)

        self.view.set_search_column(0)
        self.column.set_sort_column_id(0)

        self.view.set_reorderable(True)
        self.view.connect("cursor_changed", self.selectedCallback)

        self.add_with_viewport(self.view)

    def selectedCallback(self, tree):
        selection=self.view.get_selection()
        (model, itr)=selection.get_selected()
        device=self.store.get_value(itr, 1)
        self.gui.update_note(self.gui.manager.get_device(device))

    def find_udi(self, udi, dev):
        m=re.search(udi, dev.udi)
        if m is not None:
            return dev.udi
        if dev.has_children():
            for child in dev.children:
                r_udi=self.find_udi(udi, child)
                if r_udi is not None:
                    return r_udi


class DeviceCommon:
    def __init__(self, line):
        units=line.split(":")
        units[0]=re.sub('\s*\(\w+\)','',units[0])
        units[3]=re.sub('[@,]','_',units[3])
        self.name=units[0]
        self.udi=units[3]

    def update_udi(self, udi):
        self.udi=udi
