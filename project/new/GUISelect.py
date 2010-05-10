#!/usr/bin/env python
# example radiobuttons.py
import pygtk
pygtk.require( '2.0' )
import gtk
import pkglist

class selectDialog( object ):
    def __init__( self, parent ):
        self.value = None
        self.dialog = gtk.Dialog( "Select a package", parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, None )

        combo = gtk.Combo()
        combo.entry.set_text( '' )
        dict = pkglist.fastload()
        combotext = []
        for key in dict.keys():
            if not dict[key] in combotext:
                combotext.append( dict[key] )# + ' --- ' + key )
        combo.set_popdown_strings( combotext )
        combo.show()
        self.dialog.vbox.pack_start( combo )

        btnok = gtk.Button( 'OK' )
        self.dialog.action_area.pack_start( btnok, True, True, 0 )
        def okcallback( widget, args ):
            self.value = combo.entry.get_text()
            self.dialog.destroy()

        btnok.connect( 'clicked', okcallback, None )
        btnok.show()

        btncan = gtk.Button( 'Cancel' )
        self.dialog.action_area.pack_start( btncan, True, True, 0 )
        def cancallback( widget, args ):
            self.value = None
            self.dialog.destroy()

        btncan.connect( 'clicked', cancallback, None )
        btncan.show()

    def run( self ):
        self.dialog.run()
        return self.value

class argDialog( object ):
    def __init__( self, parent, drvname = None ):
        self.classes = None
        self.src = None
        self.dst = None
        self.drvname = drvname

        self.ident = None
        self.perm = None
        self.policy = None
        self.priv = None
        self.value = True

        self.dialog = gtk.Dialog( "Add_drv arguments", parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, None )
        table = gtk.Table( 9, 7, True )
        def bindarg( lbl, ent, count ):
            ent.select_region( 0, len( ent_class.get_text() ) )
            lbl.show()
            ent.show()
            table.attach( lbl, 1, 2, count, count + 1 )
            table.attach( ent, 3, 6, count, count + 1 )

        lbl_class = gtk.Label( "class_name" )
        ent_class = gtk.Entry()
        bindarg( lbl_class, ent_class, 4 )

        lbl_ident = gtk.Label( "identify_name" )
        ent_ident = gtk.Entry()
        bindarg( lbl_ident, ent_ident, 5 )

        lbl_permi = gtk.Label( "permission" )
        ent_permi = gtk.Entry()
        bindarg( lbl_permi, ent_permi, 6 )

        lbl_polic = gtk.Label( "policy" )
        ent_polic = gtk.Entry()
        bindarg( lbl_polic, ent_polic, 7 )

        lbl_privi = gtk.Label( "privilege" )
        ent_privi = gtk.Entry()
        bindarg( lbl_privi, ent_privi, 8 )

        table.show()
        self.dialog.vbox.pack_start( table )

        btnok = gtk.Button( 'OK' )
        self.dialog.action_area.pack_start( btnok, True, True, 0 )
        def okcallback( widget, args ):
            self.value = True
            self.classes = ent_class.get_text()
            self.ident = ent_ident.get_text()
            self.perm = ent_permi.get_text()
            self.policy = ent_polic.get_text()
            self.priv = ent_privi.get_text()
            self.dialog.destroy()

        btnok.connect( 'clicked', okcallback, None )
        btnok.show()

        btncan = gtk.Button( 'Cancel' )
        self.dialog.action_area.pack_start( btncan, True, True, 0 )
        def cancallback( widget, args ):
            self.value = False
            self.classes = None
            self.ident = None
            self.perm = None
            self.policy = None
            self.priv = None
            self.dialog.destroy()

        btncan.connect( 'clicked', cancallback, None )
        btncan.show()

    def run( self ):
        self.dialog.run()
        return ( self.value, self.classes, self.ident, self.perm, self.policy, self.priv )
