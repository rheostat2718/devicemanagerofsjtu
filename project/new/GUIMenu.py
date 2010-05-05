import pygtk
pygtk.require( "2.0" )
import gtk
import gobject
import thread

class GUIMenu( gtk.MenuBar ):
    def __init__( self, gui, manager = None ):
        gtk.MenuBar.__init__( self )

        self.gui = gui
        self.manager = manager

        # device menu
        device_menu = gtk.Menu()
        device_menu.show()

        refresh_item = gtk.MenuItem( "Refresh" )
        clear_cache_item = gtk.MenuItem( "Clear Cache" )
        edit_cache_item = gtk.MenuItem( "Edit Cache" )
        reload_cache_item = gtk.MenuItem( "Reload Cache" )
        exit_item = gtk.MenuItem( "Exit" )

        for item in ( refresh_item, clear_cache_item, edit_cache_item, reload_cache_item, exit_item ):
            device_menu.append( item )
            item.show()

        refresh_item.connect_object( "activate", self.test, "refresh" )
        clear_cache_item.connect_object( "activate", self.clearCache, "clear cache" )
        edit_cache_item.connect_object( "activate", self.editCache, "edit cache" )
        reload_cache_item.connect_object( "activate", self.reloadCache, "reload cache" )
        exit_item.connect_object( "activate", self.gui.destroy, None )

        #device menu
        device_item = gtk.MenuItem( "Device" )
        device_item.set_submenu( device_menu )
        device_item.show()

        #tools menu
        tools_menu = gtk.Menu()
        tools_menu.show()

        reconf_item = gtk.MenuItem( "Reconfigure" )
        tools_menu.append( reconf_item )
        reconf_item.show()
        reconf_item.connect_object( "activate", self.reconf, "reconfigure" )

        tools_item = gtk.MenuItem( "Tools" )
        tools_item.set_submenu( tools_menu )
        tools_item.show()

        # help menu
        help_menu = gtk.Menu()
        help_menu.show()

        help_item = gtk.MenuItem( "Help" )
        help_menu.append( help_item )
        help_item.show()

        about_item = gtk.MenuItem( "About" )
        help_menu.append( about_item )
        about_item.show()

        help_item.connect_object( "activate", self.test, "help" )
        about_item.connect_object( "activate", self.test, "about" )

        help_item_ = gtk.MenuItem( "Help" )
        help_item_.set_submenu( help_menu )
        help_item_.show()

        self.append( device_item )
        self.append( tools_item )
        self.append( help_item_ )

    def test( self, info ):
        self.manager.daemon.send("test","hi",info,"bye",info);

    def clearCache( self , info ):
        import pkglist
        pkglist.removeDump()
        if self.manager:
            self.manager.notify( info, "finished" )

    def editCache( self, info ):
        pass

    def reloadThread( self, info ):
        if self.manager:
            gobject.idle_add( self.manager.notify, info, "start" )
        import pkglist
        pkglist.run()
        if self.manager:
            gobject.idle_add( self.manager.notify, info, "finished" )

    def reloadCache( self, info ):
        thread.start_new_thread( self.reloadThread, ( info, ) )

    def reconf( self, info ):
        import tools
        ret = tools.reconfigure()
        if self.manager:
            if ret:
                self.manager.notify( info, "finished" )
            else:
                self.manager.notify( info, "failed" )
