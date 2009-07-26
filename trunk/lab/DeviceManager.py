#!/usr/bin/env python

import dbus
import dbus.glib
from dbus.mainloop.glib import DBusGMainLoop
import gobject

def changed(msg, *args):
    print msg

DBusGMainLoop(set_as_default=True)

bus=dbus.SystemBus()
obj=bus.get_object('org.freedesktop.Hal','/org/freedesktop/Hal/Manager')
mgr=dbus.Interface(obj, 'org.freedesktop.Hal.Manager')

mgr.connect_to_signal("DeviceAdded", lambda *args: changed("DeviceAdded",*args))
mgr.connect_to_signal("DeviceRemoved", lambda *args: changed("DeviceRemoved",*args))

loop=gobject.MainLoop()
loop.run()
