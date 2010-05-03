import pygtk
pygtk.require("2.0")
import gtk

class GUIMenu(gtk.MenuBar):
    def __init__(self, gui, manager=None):
        gtk.MenuBar.__init__(self)

        self.gui=gui
        self.manager=manager

        # device menu
        device_menu=gtk.Menu()
        device_menu.show()

        refresh_item=gtk.MenuItem("Refresh")
        clear_cache_item=gtk.MenuItem("Clear Cache")
        reload_item=gtk.MenuItem("Reload")
        exit_item=gtk.MenuItem("Exit")

        for item in (refresh_item, clear_cache_item, reload_item, exit_item):
            device_menu.append(item)
            item.show()

        refresh_item.connect_object("activate", self.test, "refresh")
        clear_cache_item.connect_object("activate", self.test, "clear")
        reload_item.connect_object("activate", self.test, "reaload")
        exit_item.connect_object("activate", self.gui.destroy, None)

        device_item=gtk.MenuItem("Device")
        device_item.set_submenu(device_menu)
        device_item.show()

        # help menu
        help_menu=gtk.Menu()
        help_menu.show()

        about_item=gtk.MenuItem("About")
        help_menu.append(about_item)
        about_item.show()

        help_item=gtk.MenuItem("Help")
        help_menu.append(help_item)
        help_item.show()

        about_item.connect_object("activate", self.test, "about")
        help_item.connect_object("activate", self.test, "help")

        help_item_=gtk.MenuItem("Help")
        help_item_.set_submenu(help_menu)
        help_item_.show()

        self.append(device_item)
        self.append(help_item_)

    def test(self, info):
        print 'menu test: ',info


