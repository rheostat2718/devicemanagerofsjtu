import pygtk
pygtk.require("2.0")
import gtk

class KeyAndValue(gtk.ScrolledWindow):
    def __init__(self, hash = None):
        gtk.ScrolledWindow.__init__(self)
        self.store = gtk.ListStore(str,str)
        self.view = gtk.TreeView(self.store)
        self.set_border_width(10)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.add_with_viewport(self.view)
        self.view.show()
        
        self.tv_key = gtk.TreeViewColumn('Key')
        self.view.append_column(self.tv_key)
        self.cell_key=gtk.CellRendererText()
        self.tv_key.pack_start(self.cell_key, True)
        self.tv_key.add_attribute(self.cell_key, 'text', 0)
        self.tv_key.set_sort_column_id(0)
        
        self.tv_val = gtk.TreeViewColumn('Value')
        self.view.append_column(self.tv_val)
        self.cell_val=gtk.CellRendererText()
        self.tv_val.pack_start(self.cell_val, True)
        self.tv_val.add_attribute(self.cell_val, 'text', 1)                
        self.tv_val.set_sort_column_id(0)
        
        if hash:
            self.refresh(hash)
        
    def refresh(self, hash = None):
        for (k, v) in hash.items():
            self.store.append([k,v])

def get_okcancel(parent,title,text):
    dialog = gtk.Dialog(title,parent,1)
    content = dialog.get_content_area()
    label = gtk.Label(text)
    label.show()
    content.pack_start(label)
    ret = []
    
    def action(widget,ret,b):
        ret.append(b)
        dialog.destroy()

    #buttons
    button1 = dialog.add_button(gtk.STOCK_OK,gtk.RESPONSE_ACCEPT)
    button1.connect("clicked",action,ret,True)
    button2 = dialog.add_button(gtk.STOCK_CANCEL,gtk.RESPONSE_REJECT)
    button2.connect("clicked",action,ret,False)
    dialog.run()
    return ret[0]

def get_ok(parent,title,text):
    dialog = gtk.Dialog(title,parent,1)
    content = dialog.get_content_area()
    label = gtk.Label(text)
    label.show()
    content.pack_start(label)
    
    def action(widget):
        dialog.destroy()

    #buttons
    button1 = dialog.add_button(gtk.STOCK_OK,gtk.RESPONSE_ACCEPT)
    button1.connect("clicked",action)
    dialog.run()

if __name__=='__main__':
    print get_ok(None, 'abc', 'bcd')