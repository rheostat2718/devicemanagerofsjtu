
class DeviceManagerGUI( gtk.Window ):
    def __init__( self, manager ):
        self.manager = manager

        gtk.Window.__init__( self, gtk.WINDOW_TOPLEVEL )
        self.set_title( "Device Manager v0.3" )
        self.connect( "delete_event", self.delete_event )
        self.device_tree = DeviceTree( manager.getDeviceObj( "root" ), self )
        self.device_common = CommonDeviceList( manager.getDeviceObj( "root" ), self )
        #self.top.add(self.device_tree.getFrame())
        #self.top.set_size_request(300, 400)
        #self.top.show_all()

        #self.top2=gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.top2.set_title('Note')
        self.notebook = DeviceNote()
        self.notebookleft = DeviceNoteLeft( self.device_common, self.device_tree )
        #self.top2.add(self.notebook)
        #self.top2.show_all()

        self.menu_items = ( 
            ( "/_Device", None, None, 0, "<Branch>" ),
            ( "/Device/_Refresh", "<control>R", self.print_hello, 0, None ),
            ( "/Device/_Clear cache", "<control>C", None, 0, None ),
            ( "/Device/_Upload", "<control>U", None, 0, None ),
            ( "/Device/Exit", "<control>E", gtk.main_quit, 0, None ),
            ( "/_Help", None, None, 0, "<Branch>" ),
            ( "/_Help/Help", None, None, 0, None ),
            ( "/_Help/About", None, None, 0, None ), )

        main_vbox = gtk.VBox( False, 1 )
        main_vbox.set_border_width( 1 )
        self.add( main_vbox )
        main_vbox.show()

        menubar = self.get_main_menu( self )
        main_vbox.pack_start( menubar, False, True, 0 )
        menubar.show()






        handlebox = gtk.HandleBox()
        main_vbox.pack_start( handlebox, False, False, 5 )

        toolbar = gtk.Toolbar()
        toolbar.set_orientation( gtk.ORIENTATION_HORIZONTAL )
        toolbar.set_style( gtk.TOOLBAR_BOTH )
        toolbar.set_border_width( 5 )
        handlebox.add( toolbar )

        iconw = gtk.Image()
        iconw.set_from_file( "gtk.xpm" )
        close_button = toolbar.append_item( 
            None,
            "Closes this app",
            "Private",
            iconw,
            gtk.main_quit )
        toolbar.append_space()

        iconw = gtk.Image()
        iconw.set_from_file( "gtk.xpm" )
        close_button = toolbar.append_item( 
            None,
            "Closes this app",
            "Private",
            iconw,
            gtk.main_quit )
        toolbar.append_space()








        align = gtk.Alignment( 0, 0, 0, 0 )
        main_vbox.pack_end( align, False, False, 0 )
        align.show()

        self.pbar = gtk.ProgressBar()
        align.add( self.pbar )
        self.pbar.show()

        self.timer = gobject.timeout_add ( 100, progress_timeout, self )






        self.table = gtk.Table( 1, 2 )
        #self.table.attach(self.device_tree,0,1,0,1)
        self.table.attach( self.notebookleft, 0, 1, 0, 1 )
        self.table.attach( self.notebook, 1, 2, 0, 1 )

        main_vbox.pack_start( self.table )
        #self.add(self.table)
        self.set_size_request( 800, 600 )
        self.show_all()

    def delete_event( self, widget, event, data = None ):
        gobject.source_remove( self.timer )
        self.timer = 0
        gtk.main_quit()

    def update( self ):
        self.device_tree.make_view()
        self.updateNote( self )

    def updateNote( self, device = None ):
        self.notebook.update( device )


    def loop( self ):
        pass

    def print_hello( self, w, data ):
        print "abc"

    def get_main_menu( self, window ):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory( gtk.MenuBar, "<main>", accel_group )
        item_factory.create_items( self.menu_items )
        window.add_accel_group( accel_group )
        self.item_factory = item_factory
        return item_factory.get_widget( "<main>" )

def progress_timeout( pbobj ):
    new_val = pbobj.pbar.get_fraction() + 0.01
    if new_val > 1.0:
        new_val = 0.0
    pbobj.pbar.set_fraction( new_val )
    return True
