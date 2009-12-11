import pygtk
pygtk.require( '2.0' )
import gtk
import drv
import sys

#for test
import pynotify

class DriverInfoFrame( gtk.Frame ):
    def __init__( self, devicename ):
        gtk.Frame.__init__( self )
        #self.set_label( 'Module Info' )
        self.set_label_align( 1.0, 0.0 )#left top
        #self.set_shadow_type( gtk.SHADOW_ETCHED_IN )
        self.devicename = devicename
        self.make_widgets()

    def make_list( self, d ):
        from class_DeviceManagerGUI import KeyAndValue
        self.scrolled_window = KeyAndValue( d )

    def button_test( self, widget, id ):
        icon=gtk.StatusIcon()
        icon.set_from_stock(gtk.STOCK_ABOUT)

        pynotify.init('example')
        n=pynotify.Notification(id, 'test only')
        n.attach_to_status_icon(icon)
        n.show()

    def make_widgets( self ):
        btnname = ['Refresh', 'Install', 'Uninstall', 'Update']
        self.bbox1=gtk.HButtonBox()
        self.bbox2=gtk.HButtonBox()
        self.table = gtk.Table( 10, 1, True )
        self.add( self.table )
        for name in btnname[:2]:
            btn = gtk.Button( name )
            btn.set_size_request(120,30)
            #connect
            btn.connect("clicked", self.button_test, name)
            self.bbox1.add( btn )
            btn.show()
        for name in btnname[2:]:
            btn = gtk.Button( name )
            btn.set_size_request(120,30)
            #connect
            btn.connect("clicked", self.button_test, name)
            self.bbox2.add( btn )
            btn.show()
        if self.devicename == 'unknown':
            l = {}
        else:
            d = drv.PackageDriver( self.devicename )
            l = d.info()
        self.make_list( l )
        self.table.attach( self.scrolled_window, 0, 1, 0, 8 )
        self.table.attach( self.bbox1, 0, 1, 8, 9 )
        self.table.attach( self.bbox2, 0, 1, 9, 10 )
        self.scrolled_window.show()
        self.bbox1.show()
        self.bbox2.show()
        self.table.show()

    def main( self ):
        gtk.main()

class DriverGUITest:
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
