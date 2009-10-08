import pygtk
pygtk.require( '2.0' )
import gtk
import drv
import sys

class DriverInfoFrame( gtk.Frame ):
    def __init__( self, devicename ):
        gtk.Frame.__init__( self )
        self.set_label( 'Module Info' )
        self.set_label_align( 1.0, 0.0 )#left top
        self.set_shadow_type( gtk.SHADOW_ETCHED_IN )
        self.devicename = devicename
        self.make_widgets()

    def make_list( self, d ):
        from class_DeviceManagerGUI import KeyAndValue
        self.scrolled_window = KeyAndValue( d )
        '''
        self.liststore = gtk.ListStore(str,str)
        for key in d.keys():
            self.liststore.append([key,d[key]])
        tview = gtk.TreeView(self.liststore)
        treecolumnkey = gtk.TreeViewColumn('Key')
        treecolumnvalue = gtk.TreeViewColumn('Value')
        tview.append_column(treecolumnkey)
        tview.append_column(treecolumnvalue)
        self.cell1 = gtk.CellRendererText()
        self.cell2 = gtk.CellRendererText()
        treecolumnkey.pack_start(self.cell1,True)
        treecolumnkey.add_attribute(self.cell1,'text',0)
        treecolumnvalue.pack_start(self.cell2,True)
        treecolumnvalue.add_attribute(self.cell2,'text',1)
        tview.set_search_column(0)
        treecolumnkey.set_sort_column_id(0)
        treecolumnvalue.set_sort_column_id(0)
        tview.set_reorderable(True)
        tview.show()
        '''


    def make_widgets( self ):
        btnname = ['Refresh', 'Install', 'Uninstall', 'Update', 'Backup', 'Restore']
        self.buttons = []
        self.table = gtk.Table( 2, len( btnname ), False )
        self.add( self.table )
        count = 0
        for name in btnname:
            btn = gtk.Button( name )
            self.table.attach( btn, count, count + 1, 1, 2 )
            count += 1
            self.buttons.append( btn )
            btn.show()
        ''' 
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_border_width(10)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        '''
        d = drv.Driver( self.devicename )
        l = d.getInfo( True )
        print l
        self.make_list( l )
        self.table.attach( self.scrolled_window, 0, len( btnname ), 0, 1 )
        self.scrolled_window.show()
        self.table.show()

    def main( self ):
        gtk.main()

class DriverGUITest():
    def __init__( self, devicename ):
        window = gtk.Window( gtk.WINDOW_TOPLEVEL )
        window.set_title( 'Driver GUI Test' )
        window.connect( "destroy", gtk.main_quit )
        window.set_size_request( 300, 300 )
        window.set_border_width( 10 )
        frame = DriverInfoFrame( devicename )
        window.add( frame )
        frame.show()
        window.show()

if __name__ == '__main__':
    DriverGUITest( sys.argv[1] )
    gtk.main()

"""
    def addLabelItem( self, lindent, rindent, key, value ):
        if ( type( value ) == type( str() ) ) | ( type( value ) == type( int() ) ) | ( type( value ) == type( float() ) ):
            l1 = Label( self.left, text = lindent + str( key ), fg = self.fg, bg = self.bg, font = self.leftfont )
            l2 = Label( self.right, text = rindent + str( value ), fg = self.fg, bg = self.bg, font = self.rightfont )
            self.leftlabels.append( l1 )
            self.rightlabels.append( l2 )
            l1.pack( side = TOP, anchor = NW )
            l2.pack( side = TOP, anchor = NW )
        elif ( type( value ) == type( list() ) ):
            l1 = Label( self.left, text = lindent + str( key ), fg = self.fg, bg = self.bg, font = self.leftfont )
            l2 = Label( self.right, text = rindent, fg = self.fg, bg = self.bg, font = self.rightfont )
            self.leftlabels.append( l1 )
            self.rightlabels.append( l2 )
            l1.pack( side = TOP, anchor = NW )
            l2.pack( side = TOP, anchor = NW )
            for minorvalue in value:
                self.addLabelItem( lindent + '|-', rindent + '  ', '', minorvalue )
        elif ( type( value ) == type( dict() ) ):
            l1 = Label( self.left, text = lindent + str( key ), fg = self.fg, bg = self.bg, font = self.leftfont )
            l2 = Label( self.right, text = rindent, fg = self.fg, bg = self.bg, font = self.rightfont )
            self.leftlabels.append( l1 )
            self.rightlabels.append( l2 )
            l1.pack( side = TOP, anchor = NW )
            l2.pack( side = TOP, anchor = NW )
            minorkeys = value.keys()
            minorkeys.sort()
            for minorkey in minorkeys:
                self.addLabelItem( lindent + '|', rindent + '- ', minorkey, value[minorkey] )
        else:
            print type( value )
"""
"""
TODO:
1 - anyone could make it beautiful?  ^_^||
2 - add special key to show up first, e.g 'name','size'...
3 - add sort | reverse sort | special first order
5 - add scrollbar?,listbox?
BUGFIX:
4 - find unknown type... also maybe type itself...
"""
