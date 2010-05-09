#!/usr/bin/python

import pygtk
pygtk.require( "2.0" )
import gtk

from GUIMenu import *
from GUINotebook import *
from GUIDeviceTree import *
from GUIDeviceCommon import *

class DeviceManagerGUI( gtk.Window ):
    def __init__( self, manager = None ):
        gtk.Window.__init__( self, gtk.WINDOW_TOPLEVEL )
        self.manager = manager

        # signal
        self.connect( "destroy", self.destroy )

        vbox = gtk.VBox( False, 0 )
        self.add( vbox )
        vbox.show()

        # menu
        self.menu_bar = GUIMenu( self, manager )
        menu_bar=self.menu_bar
        vbox.pack_start( menu_bar, False, False, 0 )
        menu_bar.show()



        toolbar = gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        toolbar.set_style(gtk.TOOLBAR_BOTH)
        toolbar.set_border_width(5)
        vbox.pack_start(toolbar, False, False, 0)

        iconw=gtk.Image()
        iconw.set_from_stock(gtk.STOCK_REFRESH,2)
        toolbar.append_item(None,"Reload",None,iconw, self.refresh) # TODO
        #toolbar.append_space()

        iconw=gtk.Image()
        iconw.set_from_stock(gtk.STOCK_CLOSE,2)
        toolbar.append_item(None, "Close", None, iconw, self.destroy)
        #toolbar.append_space()


        # device common & tree
        device_common = DeviceCommonList( manager.get_device( "root" ), self )
        device_tree = DeviceTree( manager.get_device( "root" ), self )

        # body
        hpan = gtk.HPaned()
        self.note_left = DeviceNoteLeft( device_tree, device_common )
        self.note_right = DeviceNoteRight(self)
        hpan.add1( self.note_left )
        hpan.add2( self.note_right )
        hpan.show()
        vbox.pack_start( hpan, True, True, 0 )

        self.show_all()

    def refresh(self, widget, data=None):
        self.menu_bar.refresh()

    def destroy( self, widget, data = None ):
        if self.manager.server==True:
            self.manager.daemon.send('quit')

        gtk.main_quit()

    def update_note( self, device ):
        self.note_right.clearPackageItem()
        self.note_right.update( device )

