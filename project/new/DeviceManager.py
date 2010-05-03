#!/usr/bin/python

import sys
import gtk
import gobject

from Device import Device
from Daemon import Daemon
from DeviceManagerGUI import DeviceManagerGUI

gobject.threads_init()

class DeviceManager( object ):
    def __init__( self ):
        self.devices = {}
        self.daemon = Daemon( self )
        self.build_device_tree()

        self.gui = DeviceManagerGUI( self )

    def build_device_tree( self ):
        for k, device in self.devices.items():
            if str( device.get( "parent" ) ) == 'None':
                self.devices["root"] = device
            else:
                self.devices[device.get( "parent" )].append_child( device )

        print "build tree done!"

    def append_device( self, device ):
        self.devices[str( device.udi )] = device

    def update_device( self, device ):
        self.devices[str( device.udi )] = device

    def get_device( self, udi ):
        return self.devices[str( udi )]

    def get_device_product( self, udi ):
        return self.devices[udi].get( "product" )

    def loop( self ):
        import threading

        self.threads = []
        self.threads.append( threading.Thread( target = self.daemon.loop ) )

        for t in self.threads:
            t.start()

    def notify( self, title, info ):
        self.daemon.notify( title, info )

    def quit( self ):
        sys.exit( 0 )


if __name__ == '__main__':
    d = DeviceManager()
    #d.loop()
    gtk.main()
