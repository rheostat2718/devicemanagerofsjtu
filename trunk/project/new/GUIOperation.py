#!/usr/bin/python

import pygtk
pygtk.require( "2.0" )
import gtk
import gobject
import thread

helpdoc = """
Device Manager Document:

To install / remove drivers, you may need root privileges.
To get package info or install / uninstall packages, network connection is needed.  

"""

class Operation( object ):
    def __init__( self, manager ):
        self.manager = manager

    def threadLongRun( self, info, func ):
        if self.manager:
            if self.manager.notify:
                gobject.idle_add( self.manager.notify, info, "start" )
        ret = func( info )
        if self.manager:
            if ( ret == True ) or ( ret == 0 ):
                gobject.idle_add( self.manager.notify, info, "finished" )
            else:
                print 'return value', ret
                gobject.idle_add( self.manager.notify, info, "failed" )

    def threadShortRun( self, info, func ):
        ret = func( info )
        if self.manager:
            if ( ret == True ) or ( ret == 0 ):
                gobject.idle_add( self.manager.notify, info, "finished" )
            else:
                print ret
                gobject.idle_add( self.manager.notify, info, "failed" )

    def clearCache( self , info ):
        import pkglist
        thread.start_new_thread( threadShortRun, ( self, info, pkglist.removeDump ) )

    def editCache( self, info ):
        pass

    def reloadCache( self, info ):
        import pkglist
        thread.start_new_thread( threadLongRun, ( self, info, pkglist.run ) )

    def select( self, info ):
        pass

    def reconf( self, info ):
        self.manager.send( 'reconf', 'Reconfigure', 'succeed', 'failed' )

    def pkginstall( self, info ):
        note = self.manager.gui.note_right
        if note.__dict__.has_key( 'drvname' ):
            try:
                pkg = note.package.pkg
                print pkg.install( self.manager.send )
            except AttributeError:
                gobject.idle_add( self.manager.notify, "package install", "failed due to no package attributes" )

    def pkguninstall( self, info ):
        note = self.manager.gui.note_right
        if note.__dict__.has_key( 'drvname' ):
            try:
                pkg = note.package.pkg
                print pkg.uninstall( self.manager.send )
            except AttributeError:
                gobject.idle_add( self.manager.notify, "package uninstall", "failed due to no package attributes" )

    def modadd( self, info ):
        note = self.manager.gui.note_right
        if note.__dict__.has_key( 'drvname' ):
            try:
                drv = note.module.drv
                print drv.install( self.manager.send )
            except AttributeError:
                gobject.idle_add( self.manager.notify, "add driver", "failed due to no driver attributes" )

    def moddel( self, info ):
        note = self.manager.gui.note_right
        if note.__dict__.has_key( 'drvname' ):
            try:
                drv = note.module.drv
                print drv.uninstall( self.manager.send )
            except AttributeError:
                gobject.idle_add( self.manager.notify, "rem driver", "failed due to no driver attributes" )

    def modup( self, info ):
        note = self.manager.gui.note_right
        if note.__dict__.has_key( 'drvname' ):
            #try:
                drv = note.module.drv
                print drv.update( self.manager.send )
            #except:
                #gobject.idle_add( self.manager.notify, "update driver", "failed due to no driver attributes" )

    def modchg( self, info ):
        pass

    def refresh( self, info ):
        pass

    def about( self, info ):

        label = gtk.Label( "Device Manager is a graphic management tool under Open Solaris.\n Copyright © 2009-2010 Shanghai Jiaotong University\nhttp://code.google.com/p/devicemanagerofsjtu" )
        dialog = gtk.Dialog( "About Device Manager", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, None )
        dialog.vbox.pack_start( label )
        label.show()
        cancelbutton = gtk.Button( "Cancel" )
        cancelbutton.connect( "clicked", gtk.main_quit, None )
        dialog.add( cancelbutton )
        cancelbutton.show()
        response = dialog.run()

    def help( self, info ):
        pass
