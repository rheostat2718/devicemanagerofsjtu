'''this class is main part of Device Manager
created @ 09.07.27 by 韩志超'''

from class_Device import Device
from class_DeviceManagerGUI import DeviceManagerGUI
from class_Daemon import Daemon

class DeviceManager(object):
    '''class of Device Manager'''
    def __init__(cls):
        '''init of DM'''
        cls.daemon=Daemon(cls)
        cls.devices=cls.getDeviceInfo()
        cls.gui=DeviceManagerGUI(cls)

    def loop(cls):
        '''loop threads and itself'''
        import threading
        cls.threads=[]
        cls.threads.append(threading.Thread(target=cls.gui.loop))
        cls.threads.append(threading.Thread(target=cls.daemon.loop))
        for t in threads:
            t.start()
        cls.threads[0].join()

    def update(cls, dev=None, from_=None):
        '''update all device'''
        cls.getDeviceInfo(dev)
        if from_!='GUI':
            gui.update()

    def getDeviceInfo(cls, dev=None):
        '''get device information
if dev==none, update all device information'''
        if cls.devices!=None:
            dict=cls.devices
        else:
            dict={}
        
        '''to be code'''
        return dict

    def addDriver(cls, dev):
        '''add driver'''
        cls.devices[dev.getPath()].addDriver()
    def removeDriver(cls, dev):
        '''remove driver'''
        cls.devices[dev.getPath()].removeDriver()
    def updateDriver(cls, dev, drv=None):
        '''update driver'''
        cls.devices[dev.getPath()].updateDriver(drv)
