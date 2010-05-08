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

        # device menu
        device_menu = gtk.Menu()
        device_menu.show()

        refresh_item = gtk.MenuItem( "Refresh" )
        clear_cache_item = gtk.MenuItem( "Clear Cache" )
        edit_cache_item = gtk.MenuItem( "Edit Cache" )
        reload_cache_item = gtk.MenuItem( "Reload Cache" )
        install_item = gtk.MenuItem( "Install / Update" )
        uninstall_item = gtk.MenuItem( "Uninstall" )

        exit_item = gtk.MenuItem( "Exit" )

        for item in ( refresh_item, clear_cache_item, edit_cache_item, reload_cache_item, install_item, uninstall_item, exit_item ):
            device_menu.append( item )
            item.show()

        refresh_item.connect_object( "activate", self.test, "refresh" )
        clear_cache_item.connect_object( "activate", self.clearCache, "clear cache" )
        edit_cache_item.connect_object( "activate", self.editCache, "edit cache" )
        reload_cache_item.connect_object( "activate", self.reloadCache, "reload cache" )
        install_item.connect_object( "activate", self.pkginstall, "install" )
        uninstall_item.connect_object( "activate", self.pkguninstall, "uninstall" )
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

        select_item = gtk.MenuItem( " Manually select a package to install:" )
        tools_menu.append( select_item )
        select_item.show()
        select_item.connect_object( "activate", self.select, "select" )

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
        self.manager.send('reconf','Reconfigure','succeeded','failed')
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
    ret=func()
    if self.manager:
        if ( ret == True ) or ( ret == 0 ):
            gobject.idle_add( self.manager.notify, info, "finished" )
        else:
            gobject.idle_add( self.manager.notify, info, "failed" )
