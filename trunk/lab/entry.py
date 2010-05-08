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
      window.set_title( "GTK Entry" )
      window.connect( "delete_event", lambda w, e: gtk.main_quit() )
      vbox = gtk.VBox( False, 0 )
      window.add( vbox )
      vbox.show()
      entry = gtk.Entry()
      entry.connect( "activate", self.enter_callback, entry )
      entry.select_region( 10, len( entry.get_text() ) )
      vbox.pack_start( entry, True, True, 0 )
      entry.show()


      button = gtk.Button( "Search" )
      button.connect( "clicked", self.enter_callback, entry )

      table = gtk.Table( 3, 3, True )
      table.attach( button, 1, 2, 1, 2 )
      vbox.add( table )

      button.show()
      table.show()
      window.show()

def main():
   gtk.main()
   return 0

if __name__ == "__main__":
   EntryExample()
   main()
