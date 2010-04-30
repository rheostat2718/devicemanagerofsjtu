#!/bin/python
import os
import sys

class confBackup( object ):
    def __init__( self ):
        pass

    def getConfList( self ):
        pass

    def backup( self, dataname ):
        pass

    def restore( self, dataname ):
        pass

class confData( object ):
    """ 
    configuration data consists of:
    
    tm: Backup time
    nm: Name
    tarname: Backup filename
    filelist: A list of files
    
    """
    def __init__( self, name = '' ):
        self.tm = time.time()
        self.nm = name

    def load( self ):
        pass
