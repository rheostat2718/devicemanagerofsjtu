import pygtk
pygtk.require( "2.0" )
import gtk
import gobject
import thread
import logging

class GUIMenu( gtk.MenuBar ):
    def __init__( self, gui, manager = None ):
        gtk.MenuBar.__init__( self )

        self.gui = gui
        self.manager = manager
        self.createMenu()

    def createMenu( self ):

        def configMenuItem( menu, item, callback, args ):
            menu.append( item )
            item.show()
            item.connect_object( "activate", callback, args )

        # device menu
        device_menu = gtk.Menu()
        device_menu.show()
        device_item = gtk.MenuItem( "Device" )
        device_item.set_submenu( device_menu )
        device_item.show()

        refresh_item = gtk.MenuItem( "Refresh" )
        configMenuItem( device_menu, refresh_item, self.test, "refresh" )
        configMenuItem( device_menu, gtk.MenuItem(), self.test, "seperator" )
        exit_item = gtk.MenuItem( "Exit" )
        configMenuItem( device_menu, exit_item, self.gui.destroy, None )

        # driver menu
        driver_menu = gtk.Menu()
        driver_menu.show()
        driver_item = gtk.MenuItem( "Driver" )
        driver_item.set_submenu( driver_menu )
        driver_item.show()

        add_item = gtk.MenuItem( "Add" )
        configMenuItem( driver_menu, add_item, self.test, "add" )
        remove_item = gtk.MenuItem( "Remove" )
        configMenuItem( driver_menu, remove_item, self.test, "remove" )
        reload_item = gtk.MenuItem( "Reload" )
        configMenuItem( driver_menu, reload_item, self.test, "reload" )
        update_item = gtk.MenuItem( "Change" )
        configMenuItem( driver_menu, update_item, self.test, "update" )
        configMenuItem( driver_menu, gtk.MenuItem(), self.test, "seperator" )
        install_item = gtk.MenuItem( "Install from package" )
        configMenuItem( driver_menu, install_item, self.test, "install" )
        uninstall_item = gtk.MenuItem( "Uninstall from package" )
        configMenuItem( driver_menu, uninstall_item, self.test, "uninstall" )

        #tools menu
        tools_menu = gtk.Menu()
        tools_menu.show()
        tools_item = gtk.MenuItem( "Tools" )
        tools_item.set_submenu( tools_menu )
        tools_item.show()

        reconf_item = gtk.MenuItem( "Reconfigure" )
        configMenuItem( tools_menu, reconf_item, self.reconf, "reconfigure" )
        configMenuItem( tools_menu, gtk.MenuItem(), self.test, "seperator" )
        clear_cache_item = gtk.MenuItem( "Clear Cache" )
        configMenuItem( tools_menu, clear_cache_item, self.clearCache, "clear cache" )
        edit_cache_item = gtk.MenuItem( "Edit Cache" )
        configMenuItem( tools_menu, edit_cache_item, self.editCache, "edit cache" )
        reload_cache_item = gtk.MenuItem( "Reload Cache" )
        configMenuItem( tools_menu, reload_cache_item, self.reloadCache, "reload cache" )
        select_item = gtk.MenuItem( "Manually select package to install" )
        configMenuItem( tools_menu, select_item, self.select, "select" )

        # help menu
        help_menu = gtk.Menu()
        help_menu.show()
        help_item_ = gtk.MenuItem( "Help" )
        help_item_.set_submenu( help_menu )
        help_item_.show()

        help_item = gtk.MenuItem( "Help" )
        configMenuItem( help_menu, help_item, self.test, "Help" )
        configMenuItem( help_menu, gtk.MenuItem(), self.test, "seperator" )
        about_item = gtk.MenuItem( "About" )
        configMenuItem( help_menu, about_item, self.test, "About" )

        self.append( device_item )
        self.append( driver_item )
        self.append( tools_item )
        self.append( help_item_ )

    def test( self, info ):
        self.manager.daemon.send( "test", "hi", info, "bye", info );

    def clearCache( self , info ):
        import pkglist
        thread.start_new_thread( threadShortRun, ( self, info, pkglist.removeDump ) )

    def editCache( self, info ):
        pass

    def reloadCache( self, info ):
        import pkglist
        thread.start_new_thread( threadLongRun, ( self, info, pkglist.run ) )

    def reconf( self, info ):
        import tools
        tools.reconfigure()
        self.manager.send( 'reconf', 'Reconfigure', 'succeeded', 'failed' )
        #import tools
        #thread.start_new_thread( threadShortRun, ( self, info, tools.reconfigure ) )

    def pkginstall( self, info ):
        pass

    def pkguninstall( self, info ):
        pass

    def select( self, info ):
        pass

    def modadd( self ):
        pass

    def moddel( self ):
        pass

    def modup( self ):
        pass

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
