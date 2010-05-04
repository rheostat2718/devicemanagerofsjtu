#!/usr/bin/python

import pygtk
pygtk.require( "2.0" )
import gtk

class DeviceNoteLeft( gtk.Notebook ):
    def __init__( self, device_tree, device_common = None ):
        gtk.Notebook.__init__( self )
        self.set_tab_pos( gtk.POS_TOP )

        if device_common != None:
            #common
            label = gtk.Label( "Common" )
            self.table0 = gtk.Table( 1, 1, False )
            self.table0.attach( device_common, 0, 1, 0, 1 )
            self.append_page( self.table0, label )

        #device tree
        label = gtk.Label( "Tree" )
        self.table1 = gtk.Table( 1, 1, False )
        self.table1.attach( device_tree, 0, 1, 0, 1 )
        self.append_page( self.table1, label )

        self.set_size_request( 300, 400 )

class DeviceNoteRight( gtk.Notebook ):
    def __init__( self ):
        gtk.Notebook.__init__( self )
        self.set_tab_pos( gtk.POS_TOP )

        #abstract
        label = gtk.Label( "Abstract" )
        self.table0 = gtk.Table( 1, 1, False )
        self.append_page( self.table0, label )

        #detail
        label = gtk.Label( "Detail" )
        self.table1 = gtk.Table( 1, 1, False )
        self.append_page( self.table1, label )

        #driver info
        label = gtk.Label( "Driver" )
        self.table2 = gtk.Table( 1, 1, False )
        self.append_page( self.table2, label )

        self.device = None

        self.connect( "switch-page", self.pageCallback )
        self.set_size_request( 400, 400 )

    def pageCallback( self, page, pagenum, par ):
        if self.device != None:
            self.update( self.device )

    def update( self, device ):
        if device == None:
            return 0;
        self.device = device

        try:
            self.abstract.destroy()
        except:
            pass

        try:
            self.detail.destroy()
        except:
            pass

        try:
            self.driver.destroy()
        except:
            pass

        self.abstract = DeviceAbstractInfo( device )
        self.detail = DeviceDetailTable( device )
        self.driver = DriverInfo( device )
        self.table0.attach( self.abstract, 0, 1, 0, 1 )
        self.table0.set_border_width( 5 )
        self.table1.attach( self.detail, 0, 1, 0, 1 )
        self.table1.set_border_width( 5 )
        self.table2.attach( self.driver, 0, 1, 0, 1 )
        self.table2.set_border_width( 5 )
        self.abstract.show()
        self.detail.show()
        self.driver.show()
        self.table0.show()
        self.table1.show()
        self.table2.show()

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
        for ( k, v ) in hash.items():
            self.store.append( [k, v] )

class DeviceDetailTable( KeyAndValue ):
    def __init__( self, device ):
        try:
            self.info = device.property_
            KeyAndValue.__init__( self, self.info )
        except:
            pass

class DriverInfo( gtk.VBox ):
    def __init__( self, device ):
        gtk.VBox.__init__( self, False, 10 )

        frame_top = gtk.Frame( "Module" )
        self.pack_start( frame_top, True, True, 5 )
        self.drvname = ''
        if device.property_.has_key( "info.solaris.driver" ):
            self.drvname = device.property_["info.solaris.driver"]
            self.module = ModuleTable( self.drvname )
            frame_top.add( self.module )
            self.module.show()

        frame_top.show()


        frame_buttom = gtk.Frame( "Package" )
        self.pack_start( frame_buttom, True, True, 5 )
        #self.package = PackageTable()
        frame_buttom.show()

class ModuleTable( KeyAndValue ):
    def __init__( self, drvname ):
        import Driver
        self.drv = Driver.Driver( drvname )
        self.info = self.drv.info()
        KeyAndValue.__init__( self, self.info )

class PackageTable( KeyAndValue ):
    def __init__( self, pkgname ):
        pass


