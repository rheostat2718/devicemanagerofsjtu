import pygtk
pygtk.require( "2.0" )
import gtk

helpdoc = """
Device Manager Document:

To install / remove drivers, you may need root privileges.
To get package info or install / uninstall packages, network connection is needed.  

"""

class HelpDialog( gtk.Dialog ):
    pass

class AboutDialog( gtk.Dialog ):
    pass
