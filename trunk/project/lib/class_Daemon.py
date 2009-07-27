'''this class defines class: Daemon'''

import dbus
import dbus.glib
from dbus.mainloop.glip import DBusGMainLoop
import gobject

class Daemon(object):
    '''daemon of device manager listening to HAL signal'''
    def __init__(cls, manager):
        '''init of daemon'''
        cls.__manager=manager

        DBusGMainLoop(set_as_default=True)
        bus=dbus.SystemBus()
        obj=bus.get_object('org.freedesktop.Hal','/org/freedesktop/Hal/Manager')
        cls.__hal_manager=dbus.Interface(obj, 'org.freedesktop.Hal.Manager')

        cls.__hal_manager.connect_to_signal('DeviceAdded', lambda *args: handle('DeviceAdded',*args))
        cls.__hal_manager.connect_to_signal('DeviceRemoved', lambda *args: handle('DeviceRemoved', *args))
        cls.__hal_manager.connect_to_signal('NewCapability', lambda *args: handle('NewCapability', *args))

    def loop(cls):
        cls.__loop=gobject.Mainloop()
        cls.__loop.run()
    
    def handle(cls, signal, udi, *args):
        '''handle of the signals'''
        if signal=='DeviceAdded':
            cls.__manager.update(udi)
            cls.panel(signal, udi)
        elif signal=='DeviceRemoved':
            cls.__manager.update(udi)
            cls.panel(signal, udi)
        elif signal=='NewCapability':
            cls.__manager.update(udi)
            [cap]=args
            cls.panel(signal, udi, cap)
