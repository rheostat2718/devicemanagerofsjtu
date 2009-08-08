'''this class is main part of Device Manager
created @ 09.07.27 by 韩志超'''

from class_Device import Device
from class_DeviceManagerGUI import *
from class_Daemon import Daemon

class DeviceManager(object):
    '''class of Device Manager'''

    def __init__(cls):
        '''init of DeviceManager'''
        cls.__devices={}
        cls.__daemon=Daemon(cls)

        #cls.__gui=DeviceManagerGUI(cls)

    def appendDeviceList(cls, device):
        cls.__devices[device.getUDI()]=device
    def updateDeviceList(cls, device):
        cls.__devices[device.getUDI()]=device
    def getDeviceObj(cls, udi):
        return cls.__devices[udi]
    def loop(cls):
        '''loop threads and itself'''
        import threading
        cls.__threads=[]
        #cls.__threads.append(threading.Thread(target=cls.__gui.loop))
        cls.__threads.append(threading.Thread(target=cls.__daemon.loop))
        for t in cls.__threads:
            t.start()
        cls.__threads[0].join()

    def update(cls, dev=None, from_=None):
        '''update all device'''
        pass#cls.__gui.update()
    def addDriver(cls, dev):
        '''add driver'''
        pass#cls.__devices[dev.getPath()].addDriver()
    def removeDriver(cls, dev):
        '''remove driver'''
        pass#cls.__devices[dev.getPath()].removeDriver()
    def updateDriver(cls, dev, drv=None):
        '''update driver'''
        pass#cls.__devices[dev.getPath()].updateDriver(drv)
    def mount(cls, dev):
        '''mount device'''
        pass#cls.__devices[dev.getPath()].mount()
    def unmount(cls, dev):
        '''unmount device'''
        pass#cls.__devices[dev.getPath()].mount()
