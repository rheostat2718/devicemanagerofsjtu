import pygtk
pygtk.require( '2.0' )
import gtk
import sys

import drv
from IPS import LocalesRun
class DriverInfoFrame( gtk.Frame ):
    def __init__( self, devname ):
        gtk.Frame.__init__( self )
        self.set_label_align( 1.0, 0.0 )#left top
        self.devname = devname
        self.drv = None
        self.module_window = None
        self.package_window = None
        self.make_widgets()
        
    def make_list(self):
        if self.devname == 'unknown' or not self.devname:
            self.drv = None
            l = {}
            p = {}
        else:
            self.drv = drv.PackageDriver(self.devname)
            l = LocalesRun(self.drv.info)
            if l.has_key('package'):
                p = l.pop('package')
            else:
                p = {}
        from class_DeviceManagerGUI import KeyAndValue
        self.module_window = KeyAndValue( l )
        self.package_window = KeyAndValue(p)
    
    def op_null(self,event,call_data):
        pass
    
    def on_refresh(self,event = None,call_data=None):
        if self.module_window:
            self.module_window.hide()
        if self.package_window:
            self.package_window.hide()
        self.module_window = None
        self.package_window = None
        self.make_list()
        self.table.attach( self.module_window, 0, 1, 1, 6 )
        self.table.attach(self.package_window,0,1,7,12)
        self.module_window.show()
        self.package_window.show()
        
    def on_install(self,event,call_data):
        if not self.drv:
            return
        from GUIcommon import get_okcancel
        ret = get_okcancel(None,'Install','Execute package install?')
        if not ret:
            return

        self.status.set_text('Installing') 

        try:
            ret = self.drv.install()
        except:
            ret = -1

        self.status.set_text('Waiting') 

        from GUIcommon import get_ok
        if ret != 0:
            get_ok(None,'Install','Install failed')
        else:
            get_ok(None,'Install','Install succeed')
        print 'return value =',ret
        self.on_refresh()
        
    def on_uninstall(self,event,call_data):
        if not self.drv:
            return
        from GUIcommon import get_okcancel
        ret = get_okcancel(None,'Uninstall','Execute package uninstall?')
        if not ret:
            return

        self.status.set_text('Uninstalling') 

        try:
            ret = self.drv.uninstall()
        except:
            ret = -1

        self.status.set_text('Waiting') 

        from GUIcommon import get_ok
        if ret != 0:
            get_ok(None,'Uninstall','Uninstall failed')
        else:
            get_ok(None,'Uninstall','Uninstall succeed')
        print 'return value =',ret
        self.on_refresh()
    
    def op_add(self,event,call_data):
#        if not self.drv:
#            return
        from GUIcommon import get_okcancel
        ret = get_okcancel(None,'Add driver','Execute add_drv?')
        if not ret:
            return

        self.status.set_text('Add_drv') 

        try:
            ret = self.drv.dbg_Adddrv()
        except:
            ret = -1

        self.status.set_text('Waiting') 

        from GUIcommon import get_ok
        if ret != 0:
            get_ok(None,'Add_drv','Add_drv failed')
        else:
            get_ok(None,'Add_drv','Add_drv succeed, you may need to reboot')

        print 'return value =',ret
        self.on_refresh()

    def op_remove(self,event,call_data):
        if not self.drv:
            return
        from GUIcommon import get_okcancel
        ret = get_okcancel(None,'Rem driver','Execute rem_drv?')
        if not ret:
            return

        self.status.set_text('Rem_drv') 

        try:
            ret = self.drv.dbg_Remdrv()
        except:
            ret = -1

    def op_reload(self,event,call_data):
        if not self.drv:
            return
        from GUIcommon import get_okcancel
        ret = get_okcancel(None,'Reload conf file','Execute update_drv?')
        if not ret:
            return

        self.status.set_text('Update_drv') 

        try:
            ret = self.drv.dbg_Updatedrv()
        except:
            ret = -1

        self.status.set_text('Waiting') 

        from GUIcommon import get_ok
        if ret != 0:
            get_ok(None,'Reload conf','Update_drv failed')
        else:
            get_ok(None,'Reload conf','Update_drv succeed')

        print 'return value =',ret
        self.on_refresh()
    
    def make_btns(self):
        btnname = ['PKG Install', 'PKG Uninstall','Refresh', 'Add','Remove','Reload conf']
        btncall = [self.on_install,self.on_uninstall,self.on_refresh,self.op_add,self.op_remove,self.op_reload]
        btnpic = [None,None,None,None,None,None]
        self.bbox1 = gtk.HButtonBox()
        self.bbox2=gtk.HButtonBox()
        for i in range(len(btnname)):
            if btnpic[i]:
                btn = gtk.Button(btnname[i],btnpic[i])
            else:
                btn = gtk.Button(btnname[i])
            btn.set_size_request(110,30)
            btn.connect("clicked",btncall[i],btnname[i])
            if i < 3:
                self.bbox1.add(btn)
            else:
                self.bbox2.add(btn)
            btn.show()
        
    def make_widgets( self ):
        self.table = gtk.Table( 15, 1, True )
        self.add( self.table )

        self.make_btns()
        
        lbl1 = gtk.Label('Module')
        lbl2 = gtk.Label('Package')
        lbl1.show()
        lbl2.show()
        self.status = gtk.Label('Waiting')
        self.status.show()

        self.on_refresh()
        
        self.table.attach(lbl1,0,1,0,1)
        self.table.attach(lbl2,0,1,6,7)

        self.table.attach( self.bbox1, 0, 1, 12, 13 )
        self.table.attach( self.bbox2, 0, 1, 13, 14 )
        self.table.attach(self.status,0,1,14,15)

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
