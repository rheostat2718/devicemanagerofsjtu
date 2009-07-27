'''this class is main part of Device Manager
created @ 09.07.27 by 韩志超'''

from class_Device import Device
from class_DeviceManagerGUI import DeviceManagerGUI
from class_Daemon import Daemon

class DeviceManager(object):
    '''class of Device Manager'''
    def __init__(cls):
        '''init of DM'''
        cls.__daemon=Daemon(cls)
        cls.__devices=cls.getDeviceInfo()
        cls.__gui=DeviceManagerGUI(cls)

    def loop(cls):
        '''loop threads and itself'''
        import threading
        cls.__threads=[]
        cls.__threads.append(threading.Thread(target=cls.__gui.loop))
        cls.__threads.append(threading.Thread(target=cls.__daemon.loop))
        for t in threads:
            t.start()
        cls.__threads[0].join()

    def update(cls, dev=None, from_=None):
        '''update all device'''
        cls.getDeviceInfo(dev)
        if from_!='GUI':
            cls.__gui.update()

    def getDeviceInfo(cls, dev=None):
        '''get device information
if dev==none, update all device information'''
        if cls.__devices!=None:
            dict=cls.__devices
        else:
            dict={}
        
        '''to be code'''
        return dict

    def addDriver(cls, dev):
        '''add driver'''
        cls.__devices[dev.getPath()].addDriver()
    def removeDriver(cls, dev):
        '''remove driver'''
        cls.__devices[dev.getPath()].removeDriver()
    def updateDriver(cls, dev, drv=None):
        '''update driver'''
        cls.__devices[dev.getPath()].updateDriver(drv)
    def mount(cls, dev):
        '''mount device'''
        cls.__devices[dev.getPath()].mount()
    def unmount(cls, dev):
        '''unmount device'''
        cls.__devices[dev.getPath()].mount()
