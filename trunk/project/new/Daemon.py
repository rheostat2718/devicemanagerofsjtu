import dbus
import dbus.glib
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import sys
import gtk
import pynotify

import c_api.client as tunnel

from Device import Device

class Daemon( object ):
    def __init__( self, manager = None ):
        if manager != None:
            self.manager = manager
        else:
            self.manager = None

        DBusGMainLoop( set_as_default = True )

        self.bus = dbus.SystemBus()
        obj = self.bus.get_object( 'org.freedesktop.Hal', '/org/freedesktop/Hal/Manager' )
        self.hal_manager = dbus.Interface( obj, 'org.freedesktop.Hal.Manager' )

        try:
            self.hal_manager.connect_to_signal( 'DeviceAdded', lambda * args:self.handle( 'DeviceAdded', *args ) )
        except:
            pass

        try:
            self.hal_manager.connect_to_signal( 'DeviceRemoved', lambda * args:self.handle( 'DeviceRemoved', *args ) )
        except:
            pass

        try:
            self.hal_manager.connect_to_signal( 'NewCapability', lambda * args:self.handle( 'NewCapability', *args ) )
        except:
            pass

        device_names = self.hal_manager.GetAllDevices()

        self.icon = gtk.StatusIcon()
        self.icon.set_from_stock( gtk.STOCK_INFO )

        for name in device_names:
            try:
                self.add_dev_sig_recv( name )
                device_dbus_obj = self.bus.get_object( 'org.freedesktop.Hal', name )
                properties = device_dbus_obj.GetAllProperties( dbus_interface = "org.freedesktop.Hal.Device" )

                d = Device( name, properties )
                if manager != None:
                    self.manager.append_device( d )

                self.add_dev_sig_recv( name )
            except:
                pass


    def update( self ):
        device_names = self.hal_manager.GetAllDevices()
        self.manager.device = {}
        for name in device_names:
            device_dbus_obj = self.bus.get_object( 'org.freedesktop.Hal', name )
            properties = device_dbus_obj.GetAllProperties( dbus_interface = "org.freedesktop.Hal.Device" )
            d = Device( name, properties )
            self.manager.append_device( d )
            self.add_dev_sig_recv( name )


    def add_dev_sig_recv( self, udi ):
        self.bus.add_signal_receiver( lambda * args: self.property_modified( udi, *args ), "PropertyModified", "org.freedesktop.Hal.Device", "org.freedesktop.Hal", udi )

    def property_modified( self, udi, num_changed, change_list ):
        print udi, num_changed, change_list
        pass

    #def loop( self ):
    #    self.loop = gobject.MainLoop()
    #    self.loop.run()

    def send( self, cmd, title = None, info_succ = "succeeded", info_fail = "failed" ):
        import threading
        if ( self.manager.server == False):
            m_thread = threading.Thread( target = self.start_server )
            m_thread.start()
            self.manager.server = True
        if cmd=='reconf':
            result=tunnel.send(cmd)
            gobject.idle_add(self.notify, title, result)
        else:
            m_thread = threading.Thread( target = self._send, args = ( cmd, title, info_succ, info_fail, ) )
            m_thread.start()
        #gobject.idle_add(self._send, cmd,title,info_succ, info_fail)

    def _send( self, cmd, title, info_succ='succeeded', info_fail='failed' ):
        if self.manager.server:
            import time
            time.sleep(1)
        if title != None:
            result=tunnel.send( cmd )
            #result='succeeded'
            if result == 'succeeded':
                gobject.idle_add( self.notify, title, 'succeeded' )
            if result == 'wait':
                gobject.idle_add( self.notify, title, 'please wait, it\'s running for you')
                import time
                while result=='wait':
                    time.sleep(1)
                    result=tunnel.send('query')
                gobject.idle_add(self.notify, title,result)
            else:
                gobject.idle_add( self.notify, title, 'failed' )
        else:
            tunnel.send( cmd )

    def notify( self, title, info ):
        pynotify.init( 'devicemanager' )
        n = pynotify.Notification( title, info )
        n.attach_to_status_icon( self.icon )
        n.show()

    def handle( self, signal, udi, *args ):
        self.notify( str( signal ), self.manager.get_device( udi ).get( 'product' ) )
        pass

    def start_server( self ):
        import os
        #print "server start"
        os.system( 'gksu c_api/server' )
        #print "server end"


if __name__ == '__main__':
    d = Daemon( None )
    d.loop()
