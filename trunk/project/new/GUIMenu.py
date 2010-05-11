import pygtk
pygtk.require( "2.0" )
import gtk
import gobject
import thread
#import logging

class GUIMenu( gtk.MenuBar ):
    def __init__( self, gui, manager = None ):
        gtk.MenuBar.__init__( self )

        self.gui = gui
        self.manager = manager
        if manager:
            self.opt = manager.opt
        else:
            self.opt = None
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
        configMenuItem( device_menu, refresh_item, self.opt.refresh, "refresh" )
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
        configMenuItem( driver_menu, add_item, self.opt.modadd, "add" )
        remove_item = gtk.MenuItem( "Remove" )
        configMenuItem( driver_menu, remove_item, self.opt.moddel, "remove" )
        reload_item = gtk.MenuItem( "Reload" )
        configMenuItem( driver_menu, reload_item, self.opt.modup, "reload" )
        #update_item = gtk.MenuItem( "Change" )
        #configMenuItem( driver_menu, update_item, self.opt.modchg, "update" )
        configMenuItem( driver_menu, gtk.MenuItem(), self.test, "seperator" )
        install_item = gtk.MenuItem( "Install from package" )
        configMenuItem( driver_menu, install_item, self.opt.pkginstall, "install" )
        uninstall_item = gtk.MenuItem( "Uninstall from package" )
        configMenuItem( driver_menu, uninstall_item, self.opt.pkguninstall, "uninstall" )

        #tools menu
        tools_menu = gtk.Menu()
        tools_menu.show()
        tools_item = gtk.MenuItem( "Tools" )
        tools_item.set_submenu( tools_menu )
        tools_item.show()

        reconf_item = gtk.MenuItem( "Reconfigure" )
        configMenuItem( tools_menu, reconf_item, self.opt.reconf, "reconfigure" )
        configMenuItem( tools_menu, gtk.MenuItem(), self.test, "seperator" )
        clear_cache_item = gtk.MenuItem( "Clear Cache" )
        configMenuItem( tools_menu, clear_cache_item, self.opt.clearCache, "clear cache" )
        edit_cache_item = gtk.MenuItem( "Edit Cache" )
        configMenuItem( tools_menu, edit_cache_item, self.opt.editCache, "edit cache" )
        reload_cache_item = gtk.MenuItem( "Reload Cache" )
        configMenuItem( tools_menu, reload_cache_item, self.opt.reloadCache, "reload cache" )
        select_item = gtk.MenuItem( "Manually select package to install" )
        configMenuItem( tools_menu, select_item, self.opt.select, "select" )

        # help menu
        help_menu = gtk.Menu()
        help_menu.show()
        help_item_ = gtk.MenuItem( "Help" )
        help_item_.set_submenu( help_menu )
        help_item_.show()

        help_item = gtk.MenuItem( "Help" )
        configMenuItem( help_menu, help_item, self.opt.help, "Help" )
        configMenuItem( help_menu, gtk.MenuItem(), self.test, "seperator" )
        about_item = gtk.MenuItem( "About" )
        configMenuItem( help_menu, about_item, self.opt.about, "About" )

        self.append( device_item )
        self.append( driver_item )
        self.append( tools_item )
        self.append( help_item_ )

    def test( self, info ):
        if info != "seperator":
            self.manager.daemon.send( "test", info, "hi", "bye" );
