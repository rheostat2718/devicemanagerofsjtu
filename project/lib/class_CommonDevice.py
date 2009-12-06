import os
import re
import gtk

from class_DeviceManagerGUI import *

class CommonDeviceList(gtk.ScrolledWindow):
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
                common_device=CommonDevice(line)
                common_device.update_udi(self.find_udi(common_device.udi, self.root))
                if common_device.udi is not None:
                    self.list[common_device.name]=common_device.udi
        txt.close()

    def find_udi(self, udi, dev):
        m=re.search(udi, dev.getUDI())
        if m is not None:
            return dev.getUDI()
        if dev.hasChildren():
            for child in dev.getChildren():
                r_udi=self.find_udi(udi, child)
                if r_udi is not None:
                    return r_udi


class CommonDevice:
    def __init__(self, line):
        units=line.split(":")
        units[0]=re.sub('\s*\(\w+\)','',units[0])
        units[3]=re.sub('[@,]','_',units[3])
        self.name=units[0]
        self.udi=units[3]

    def update_udi(self, udi):
        self.udi=udi
