#!/usr/bin/python

import pygtk
pygtk.require( "2.0" )
import gtk
import thread
import gobject
import threading

class DeviceNoteLeft( gtk.Notebook ):
    def __init__( self, device_tree, device_common = None ):
        gtk.Notebook.__init__( self )
        self.set_tab_pos( gtk.POS_TOP )

        if device_common:
            #common
            label = gtk.Label( "Common" )
            self.table0 = gtk.Table( 1, 1, False )
            self.table0.attach( device_common, 0, 1, 0, 1 )
            self.append_page( self.table0, label )

        if device_tree:
            #device tree
            label = gtk.Label( "Tree" )
            self.table1 = gtk.Table( 1, 1, False )
            self.table1.attach( device_tree, 0, 1, 0, 1 )
            self.append_page( self.table1, label )

        self.set_size_request( 300, 400 )

class DeviceNoteRight( gtk.Notebook ):
    def __init__( self, gui ):
        gtk.Notebook.__init__( self )
        self.gui = gui


        self.set_tab_pos( gtk.POS_TOP )

        #abstract
        self.table0 = gtk.Table( 1, 1, False )
        self.append_page( self.table0, gtk.Label( "Abstract" ) )

        #detail
        self.table1 = gtk.Table( 1, 1, False )
        self.append_page( self.table1, gtk.Label( "Detail" ) )

        #module
        self.table2 = gtk.Table( 1, 1, False )
        self.append_page( self.table2, gtk.Label( "Module" ) )

        #package1
        self.table3 = gtk.Table( 1, 1, False )
        self.append_page( self.table3, gtk.Label( "Package" ) )

        self.table0.set_border_width( 5 )
        self.table1.set_border_width( 5 )
        self.table2.set_border_width( 5 )
        self.table3.set_border_width( 5 )

        self.connect( "switch-page", self.pageCallback )
        self.set_size_request( 400, 400 )

        self.device = None
        self.callid = 0
        self.lock = threading.Lock()
        self.clearPackageItem()

    def clearPackageItem( self ):
        self.lock.acquire()
        self.callid = self.callid + 1
        self.once = True
        try:
            self.package.destroy()
        except:
            pass
        self.package = None
        self.lock.release()

    def pageCallback( self, page, pagenum, par ):
        if self.device != None:
            self.update( self.device )

    def update( self, device ):
        if device == None:
            return

        try:
            self.abstract.destroy()
            del self.abstract
        except:
            pass

        try:
            self.detail.destroy()
            del self.detail
        except:
            pass

        try:
            self.module.destroy()
            del self.module
        except:
            pass

        try:
            self.fpackage.destroy()
            del self.fpackage
        except:
            pass

        self.device = device
        self.drvname = ''
        if device.property_.has_key( "info.solaris.driver" ):
            self.drvname = device.property_["info.solaris.driver"]

        self.abstract = DeviceAbstractInfo( device )
        self.detail = DeviceDetailTable( device )
        if self.drvname:
            self.module = ModuleTable( self.gui, self.drvname )
        else:
            self.module = NullTable( self.drvname )
        self.fpackage = NullTable( self.drvname )


        self.table0.attach( self.abstract, 0, 1, 0, 1 )
        self.table1.attach( self.detail, 0, 1, 0, 1 )
        self.table2.attach( self.module, 0, 1, 0, 1 )
        self.abstract.show()
        self.detail.show()
        self.module.show()
        self.table0.show()
        self.table1.show()
        self.table2.show()

        self.lock.acquire()
        if self.package:
            self.table3.attach( self.package, 0, 1, 0, 1 )
        else:
            self.table3.attach( self.fpackage, 0, 1, 0, 1 )

        if self.package:
            self.package.show()
        else:
            self.fpackage.show()
        self.table3.show()
        id = self.callid
        self.lock.release()

        if self.once:
            if self.drvname:
                gobject.idle_add( self.gui.manager.notify, 'Pkg', 'gathering information' )
            thread.start_new_thread( self.PackageThread, ( id, ) )

    def PackageThread( self, callid ):
        if self.drvname:
            self.once = False
            if not self.package:
                import Package
                pkg = PackageTable( self.gui, self.drvname )
                self.lock.acquire()
                if callid != self.callid:
                    self.lock.release()
                    thread.exit()
                self.lock.release()
                self.package = pkg
                gobject.idle_add( self.gui.manager.notify, 'Pkg', 'finished gathering' )
                gobject.idle_add( self.update, self.device )

class DeviceAbstractInfo( gtk.VBox ):
    def __init__( self, device ):
        gtk.VBox.__init__( self, False, 5 )

        frame_top = gtk.Frame( "Device" )
        self.pack_start( frame_top, False, False, 5 )
        frame_top.show()

        table = gtk.Table( device.get_key_info_length(), 2, False )
        frame_top.add( table )
        table.show()
        t_row = 0

        for ( k, v ) in device.key_info.items():
            lbl_name = gtk.Label( k )
            lbl_name.show()
            lbl_value = gtk.Label( v )
            lbl_value.show()
            table.attach( lbl_name, 0, 1, t_row, t_row + 1, 0, 0, 5, 5 )
            table.attach( lbl_value, 1, 2, t_row, t_row + 1, 0, 0, 5, 5 )
            t_row += 1

        #TODO

class KeyAndValue( gtk.ScrolledWindow ):
    def __init__( self, hash = None ):
        gtk.ScrolledWindow.__init__( self )
        self.store = gtk.ListStore( str, str )
        self.view = gtk.TreeView( self.store )
        self.set_border_width( 5 )
        self.set_policy( gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS )
        self.add_with_viewport( self.view )
        self.view.show()

        self.tv_key = gtk.TreeViewColumn( 'Key' )
        self.view.append_column( self.tv_key )
        self.cell_key = gtk.CellRendererText()
        self.tv_key.pack_start( self.cell_key, True )
        self.tv_key.add_attribute( self.cell_key, 'text', 0 )
        self.tv_key.set_sort_column_id( 0 )

        self.tv_val = gtk.TreeViewColumn( 'Value' )
        self.view.append_column( self.tv_val )
        self.cell_val = gtk.CellRendererText()
        self.tv_val.pack_start( self.cell_val, True )
        self.tv_val.add_attribute( self.cell_val, 'text', 1 )
        self.tv_val.set_sort_column_id( 0 )

        if hash:
            self.refresh( hash )

    def refresh( self, hash = None ):
        if hash:
            hashlist = hash.keys()
            hashlist.sort()
            for k in hashlist:
                self.store.append( [k, hash[k]] )

class DeviceDetailTable( KeyAndValue ):
    def __init__( self, device ):
        try:
            self.info = device.property_
            KeyAndValue.__init__( self, self.info )
        except:
            pass

class ModuleTable( gtk.Table ):
    def __init__( self, gui, drvname ):
        self.gui = gui
        gtk.Table.__init__( self, 10, 4, False )

        import Driver
        self.drv = Driver.Driver( drvname )
        self.info = self.drv.info()
        kv = KeyAndValue( self.info )
        kv.show()
        self.attach( kv, 0, 4, 0, 9 )

        b_add = gtk.Button( 'Add' )
        b_add.connect( 'clicked', self.callback_add, drvname )
        b_add.show()
        self.attach( b_add, 0, 1, 9, 10 )

        b_rem = gtk.Button( 'Remove' )
        b_rem.connect( 'clicked', self.callback_rem, drvname )
        b_rem.show()
        self.attach( b_rem, 1, 2, 9, 10 )

        b_reload = gtk.Button( 'Reload' )
        b_reload.show()
        self.attach( b_reload, 2, 3, 9, 10 )

        b_change = gtk.Button( 'Change' )
        b_change.show()
        self.attach( b_change, 3, 4, 9, 10 )

        self.show()
    def callback_add( self, widget, data = None ):
        self.gui.manager.opt.modadd( data )

    def callback_rem( self, widget, data = None ):
        self.gui.manager.opt.moddel( data )

    def callback_update( self, widget, data = None ):
        self.gui.manager.opt.modup( data )


class NullTable( KeyAndValue ):
    def __init__( self, drvname = None ):
        if drvname:
            KeyAndValue.__init__( self, {'module.Name':drvname, 'status':'running pkg info to gather package information...' } )
        else:
            KeyAndValue.__init__( self, {} )

class PackageTable( gtk.Table ):
    def __init__( self, gui, drvname, pkgname = None ):
        self.gui = gui
        gtk.Table.__init__( self, 10, 2, False )

        b_install = gtk.Button( 'PKG Install' )
        b_install.connect( 'clicked', self.callback_install, None )
        b_install.show()
        self.attach( b_install, 0, 1, 9, 10 )

        b_uninstall = gtk.Button( 'PKG Uninstall' )
        b_uninstall.connect( 'clicked', self.callback_uninstall, None )
        b_uninstall.show()
        self.attach( b_uninstall, 1, 2, 9, 10 )

        self.show()

        import Package
        self.pkg = Package.Package( drvname, pkgname )
        self.info = self.pkg.info()
        kv = KeyAndValue( self.info )
        kv.show()
        self.attach( kv, 0, 2, 0, 9 )



    def callback_install( self, widget, data = None ):
        self.gui.manager.opt.pkginstall( data )

    def callback_uninstall( self, widge, data = None ):
        self.gui.manager.opt.pkguninstall( data )

    def threadLongRun( self, info, func ):
        if self.manager:
            if self.manager.notify:
                gobject.idle_add( self.manager.notify, info, "start" )
        ret = func()
        if self.manager:
            if ( ret == True ) or ( ret == 0 ):
                gobject.idle_add( self.manager.notify, info, "finished" )
            else:
                gobject.idle_add( self.manager.notify, info, "failed" )

    def threadShortRun( self, info, func ):
        ret = func()
        if self.manager:
            if ( ret == True ) or ( ret == 0 ):
                gobject.idle_add( self.manager.notify, info, "finished" )
            else:
                gobject.idle_add( self.manager.notify, info, "failed" )
