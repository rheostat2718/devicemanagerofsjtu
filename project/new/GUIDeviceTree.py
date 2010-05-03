import pygtk
pygtk.require("2.0")
import gtk


class DeviceTree(gtk.ScrolledWindow):
    def __init__(self, root, gui):
        self.gui=gui
        self.root=root
        gtk.ScrolledWindow.__init__(self)
        self.set_border_width(10)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.make_view()

    def make_view(self):
        try:
            self.tree_store.destroy()
            self.tree_view.destroy()
        except:
            pass

        self.make_tree()
        self.tree_view=gtk.TreeView(self.tree_store)

        self.tv_column=gtk.TreeViewColumn('Devices')
        self.tree_view.append_column(self.tv_column)

        self.cell=gtk.CellRendererText()
        self.tv_column.pack_start(self.cell, True)
        self.tv_column.add_attribute(self.cell, 'text', 0)

        self.tree_view.set_search_column(0)
        self.tv_column.set_sort_column_id(0)

        self.tree_view.set_reorderable(True)
        self.tree_view.expand_all()
        self.tree_view.connect("cursor_changed", self.selected_callback)

        self.add_with_viewport(self.tree_view)
        self.set_size_request(300,400)

    def selected_callback(self, tree):
        selection=self.tree_view.get_selection()
        (model, itr) = selection.get_selected()
        device=self.tree_store.get_value(itr,1)
        #DeviceDetailTable(self.gui.manager.getDeviceObj(device))
        self.gui.update_note(self.gui.manager.get_device(device))

    def make_tree(self):
        self.tree_store=gtk.TreeStore(str, str)
        itr=self.tree_store.append(None, [self.root.get("product"), self.root.udi])
        self.append_device(itr, self.root)

    def append_device(self, parent, device):
        for child in device.children:
            itr=self.tree_store.append(parent, [child.get("product"), child.udi])
            if child.has_children():
                self.append_device(itr, child)
