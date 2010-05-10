#!/usr/bin/env python
# example entry.py
import pygtk
pygtk.require( '2.0' )
import gtk
class EntryExample:
   def enter_callback( self, widget, entry ):
      entry_text = entry.get_text()
      print "Entry contents: %s\n" % entry_text

   def __init__( self ):
      window = gtk.Window( gtk.WINDOW_TOPLEVEL )
      window.set_size_request( 200, 100 )
      window.set_title( "Add driver" )
      window.connect( "delete_event", lambda w, e: gtk.main_quit() )
      vbox = gtk.VBox( False, 0 )
      window.add( vbox )
      vbox.show()

      label = gtk.Label( "args" )

      entry = gtk.Entry()
      entry.connect( "activate", self.enter_callback, entry )
      entry.select_region( 10, len( entry.get_text() ) )

      buttonok = gtk.Button( "OK" )
      buttonok.connect( "clicked", self.enter_callback, entry )

      buttoncan = gtk.Button( "Cancel" )
      buttoncan.connect( "clicked", gtk.main_quit, None )

      table = gtk.Table( 4, 4, True )
      table.attach( label, 0, 1, 0, 1 )
      table.attach( entry, 1, 4, 0, 1 )
      table.attach( buttonok, 1, 2, 2, 3 )
      table.attach( buttoncan, 2, 3, 2, 3 )
      vbox.add( table )

      buttonok.show()
      buttoncan.show()
      label.show()
      entry.show()
      table.show()
      window.show()

def main():
   gtk.main()
   return 0

if __name__ == "__main__":
   EntryExample()
   main()
