import pygtk
pygtk.require( '2.0' )
import gtk
import sys

#for test
import pynotify


import drv


class DriverInfoFrame( gtk.Frame ):
    def __init__( self, devname ):
        gtk.Frame.__init__( self )
        self.set_label_align( 1.0, 0.0 )#left top
        self.devname = devname
        self.make_widgets()
        self.drv = None

    def make_list(self):
        if self.devname == 'unknown' or not self.devname:
            self.drv = None
            l = {}
            p = {}
        else:
            self.drv = drv.PackageDriver(self.devname)
            l = self.drv.info()
            if l.has_key('package'):
                p = l.pop('package')
            else:
                p = {}
        from class_DeviceManagerGUI import KeyAndValue
        self.module_window = KeyAndValue( l )
        self.package_window = KeyAndValue(p)

    def button_test( self, widget, id ):
        icon=gtk.StatusIcon()
        icon.set_from_stock(gtk.STOCK_ABOUT)

        pynotify.init('example')
        n=pynotify.Notification(id, 'test only')
        n.attach_to_status_icon(icon)
        n.show()
    
    def op_null(self,event,call_data):
        pass
    
    def on_refresh(self,event,call_data):
        self.module_window.hide()
        self.package_window.hide()
        self.module_window = None
        self.package_window = None
        self.make_list()
        self.table.attach( self.module_window, 0, 1, 1, 6 )
        self.table.attach(self.package_window,0,1,7,12)
        self.module_window.show()
        self.package_window.show()
        
    def on_install(self):
        if False:
            self.drv.install()
        else:
            pass

    def make_btns(self):
        btnname = ['Refresh', 'PKG Install', 'PKG Uninstall', 'PKG Update']
        btncall = [self.on_refresh,self.op_null,self.op_null,self.op_null]
        btnpic = [None,None,None,None]
        self.bbox1 = gtk.HButtonBox()
        self.bbox2=gtk.HButtonBox()
        for i in range(len(btnname)):
            if btnpic[i]:
                btn = gtk.Button(btnname[i],btnpic[i])
            else:
                btn = gtk.Button(btnname[i])
            btn.set_size_request(110,30)
            btn.connect("clicked",btncall[i],btnname[i])
            if i < 2:
                self.bbox1.add(btn)
            else:
                self.bbox2.add(btn)
            btn.show()
        
    def make_widgets( self ):
        self.table = gtk.Table( 14, 1, True )
        self.add( self.table )

        self.make_btns()
        self.make_list()
        
        lbl1 = gtk.Label('Module')
        lbl2 = gtk.Label('Package')
        lbl1.show()
        lbl2.show()
        
        self.table.attach(lbl1,0,1,0,1)
        self.table.attach(lbl2,0,1,6,7)
        self.table.attach( self.module_window, 0, 1, 1, 6 )
        self.table.attach(self.package_window,0,1,7,12)
        self.table.attach( self.bbox1, 0, 1, 12, 13 )
        self.table.attach( self.bbox2, 0, 1, 13, 14 )

        self.module_window.show()
        self.package_window.show()
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
