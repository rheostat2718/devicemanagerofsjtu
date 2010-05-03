import dbus
import dbus.glib
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import sys
import gtk
import pynotify
from Device import Device

class Daemon(object):
    def __init__(self, manager=None):
        if manager!=None:
            self.manager=manager
        else:
            self.manager=None

        DBusGMainLoop(set_as_default=True)

        self.bus=dbus.SystemBus()
        obj=self.bus.get_object('org.freedesktop.Hal','/org/freedesktop/Hal/Manager')
        self.hal_manager=dbus.Interface(obj, 'org.freedesktop.Hal.Manager')

        self.hal_manager.connect_to_signal('DeviceAdded',   lambda *args:self.handle('DeviceAdded', *args))
        self.hal_manager.connect_to_signal('DeviceRemoved', lambda *args:self.handle('DeviceRemoved', *args))
        self.hal_manager.connect_to_signal('NewCapability', lambda *args:self.handle('NewCapability', *args))

        device_names=self.hal_manager.GetAllDevices()

        self.icon=gtk.StatusIcon()
        self.icon.set_from_stock(gtk.STOCK_ABOUT)

        for name in device_names:
            self.add_dev_sig_recv(name)
            device_dbus_obj=self.bus.get_object('org.freedesktop.Hal', name)
            properties=device_dbus_obj.GetAllProperties(dbus_interface="org.freedesktop.Hal.Device")
            if manager!=None:
                self.manager.append_device(Device(name, properties))

    def add_dev_sig_recv(self, udi):
        self.bus.add_signal_receiver(lambda *args: self.property_modified(udi, *args), "PropertyModified", "org.freedesktop.Hal.Device", "org.freedesktop.Hal", udi)

    def property_modified(self, udi, num_changed, change_list):
        #TODO
        print 'in property_modified'
        print udi, num_changed,change_list
        pass

    def loop(self):
        self.loop=gobject.MainLoop()
        self.loop.run()

    def notify(self, title, info):
        pynotify.init('dev')
        n=pynotify.Notification(title, info)
        n.attach_to_status_icon(self.icon)
        n.show()

    def handle(self, signal, udi, *args):
        #TODO
        self.notify(str(signal), str(udi))
        pass

if __name__=='__main__':
    d=Daemon(None)
    d.loop()
