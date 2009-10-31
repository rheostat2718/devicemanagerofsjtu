import sys
import pygtk
pygtk.require( '2.0' )
import gtk

class DriverInfoFrame( gtk.Frame ):
    """
        This class gather driver information and several operations
        about a specific device in a gtk.Frame.
    """
    def __init__( self, drvname) :
        gtk.Frame.__init__( self )
        self.drvname = drvname
        
        from drv import Driver
        self.drv = Driver(self.drvname)
        
        self.btnlist = [['Refresh',0,None],
                        ['Install',0,None],
                        ['Uninstall',0,None],
                        ['Update',0,None],
                        ['Backup',0,None],
                        ['Restore',0,None]]
        self.set_label( 'Driver Information' ) #Frame title
        self.set_label_align( 1.0, 0.0 ) #top-left corner
        self.set_shadow_type( gtk.SHADOW_ETCHED_IN )
        self.make_widgets()

    def make_widgets( self ):
        table = gtk.Table( 2, len( self.btnlist ), False )
        self.add( table )

        count = 0
        for item in self.btnlist:
            item[2] = gtk.Button( item[0] )
            table.attach( item[2], count, count + 1, 1, 2 )
            item[2].show()
            count += 1

        # Given argument "False" drv.Driver doesn't search related package
        # and provide fast loading
        self.info1 = self.drv.getInfo(False)     
        from GUIcommon import KeyAndValue
        self.list = KeyAndValue( self.info1 )
        
        table.attach( self.list, 0, len( self.btnlist ), 0, 1 )

        self.list.show()
        table.show()

    def force_refresh(self):
        self.drv = Driver(self.drvname)
        self.refresh_list()

    def refresh_list(self):
        if self.drv:
            self.info1 = self.drv.getInfo( False )
        else:
            self.info1 = None
        self.list.refresh(self.info1)

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

TODO:
1 - anyone could make it beautiful?  ^_^||
2 - add special key to show up first, e.g 'name','size'...
3 - add sort | reverse sort | special first order
5 - add scrollbar?,listbox?
BUGFIX:
4 - find unknown type... also maybe type itself...
"""
