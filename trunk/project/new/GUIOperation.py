#!/usr/bin/python
#coding:utf-8
import pygtk
pygtk.require( "2.0" )
import gtk
import gobject
import thread

helpdoc = """
Device Manager Usage:

Device -> Refresh : refresh device trees and device info.
Device -> Exit : exit the program.
Driver -> Add : execute add_drv.
Driver -> Remove : execute rem_drv.
Driver -> Reload : execute update_drv.

Driver -> Install from packages : use pkg install to install / update driver files.
Driver -> Uninstall from packages : use pkg uninstall to remove driver files.
Tools -> Reconfigure : execute touch reconfigure.
Tools -> Clear cache : clean up cache file.
Tools -> Edit cache : manually edit cache file.
Tools -> Reload cache : generate cache file from remote package repository.
Tools -> Manually select package to install : select from a driver-related package list to install.
Help -> Help : display this document.
Help -> About : display about document.
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
        thread.start_new_thread( self.threadShortRun, ( info, pkglist.removeDump ) )

    def editCache( self, info ):
        import pkglist
        thread.start_new_thread( self.threadLongRun, ( info, pkglist.editCache ) )

    def reloadCache( self, info ):
        import pkglist
        thread.start_new_thread( self.threadLongRun, ( info, pkglist.run ) )

    def select( self, info ):
        import GUISelect
        dialog = GUISelect.selectDialog( self.manager.gui )
        ret = dialog.run()
        if not ret:
            return
        #print ret
        import Package
        pkg = Package.Package()
        pkg.setPkgname( ret )
        pkg.install( self.manager.send )

    def reconf( self, info ):
        self.manager.send( 'reconf', 'Reconfigure', 'succeeded', 'failed' )

    def pkginstall( self, info ):
        note = self.manager.gui.note_right
        func = None
        try:
            func = note.package.pkg.install
        except AttributeError:
            self.manager.notify( "Package install", "Failed due to no related package." )
        func( self.manager.send )

    def pkguninstall( self, info ):
        note = self.manager.gui.note_right
        func = None
        try:
            func = note.package.pkg.uninstall
        except AttributeError:
            self.manager.notify( "Package uninstall", "Failed due to no related package." )
        func( self.manager.send )

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
            try:
                drv = note.module.drv
                print drv.update( self.manager.send )
            except AttributeError:
                gobject.idle_add( self.manager.notify, "update driver", "failed due to no driver attributes" )

    def modchg( self, info ):
        drvname = None
        try:
            drvname = self.manager.gui.note_right.drvname
        except AttributeError:
            pass
        import GUISelect

        dialog = GUISelect.argDialog( self.manager.gui, drvname )
        ret = dialog.run()
        if not ret[0] or not ret[1]:
            return
        #print ret
        #src = 2, dst  = 3 file = 4 cimpp=56789
        import Driver
        drv = Driver.Driver( ret[1] )
        drv.install( self.manager.send, ret[4], ret[2], ret[3], ret[5:9] )

    def refresh( self, info ):
        self.manager.gui.refresh( None )

    def about( self, info ):

        label = gtk.Label( "Device Manager is a graphic device management tool under OpenSolaris.\n Copyright © 2009-2010 Shanghai Jiaotong University.\nLatest source code can be downloaded at : http://devicemanagerofsjtu.googlecode.com/svn/ \n and at opensolaris community :" )
        dialog = gtk.Dialog( "About Device Manager", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, None )
        dialog.vbox.pack_start( label )
        label.show()

        btncan = gtk.Button( 'Close' , stock = gtk.STOCK_CLOSE )
        dialog.action_area.pack_start( btncan, True, True, 0 )
        def cancallback( widget, dialog ):
            dialog.destroy()

        btncan.connect( 'clicked', cancallback, dialog )
        btncan.show()
        response = dialog.run()

    def help( self, info ):
        label = gtk.Label( helpdoc )
        dialog = gtk.Dialog( "Help", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, None )
        dialog.vbox.pack_start( label )
        label.show()
        btncan = gtk.Button( 'Close', stock = gtk.STOCK_CLOSE )
        dialog.action_area.pack_start( btncan, True, True, 0 )
        def cancallback( widget, dialog ):
            dialog.destroy()

        btncan.connect( 'clicked', cancallback, dialog )
        btncan.show()
        response = dialog.run()
