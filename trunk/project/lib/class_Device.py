'''this class is the definition of class: Device
created @ 09.07.27 by 韩志超'''

class Device(object):
    '''class of Device
    di_node
    udi/path
    device_type
    vendor_name
    device_name/model
    driver_name # libdevinfo
    driver_ops # libdevinfo
    driver_major # libdevinfo
    properties
    '''

    SERVICE='org.freedesktop.Hal'
    INTERFACE='org.freedesktop.Hal.Device'

    def __init__(cls, udi, property_=None):
        cls.__udi=udi
        if property_==None:
            cls.__property={}
        else:
            print udi, property_
            cls.__property=property_

    def updateProperty(cls, p):
        cls.__priperty=p

    def setProperty(cls, p, value):
        cls.__property[p]=value
    def getProperty(cls, p):
        return cls.__property[p]
    def remProperty(cls, p):
        try:
            del cls.property[p]
        except:
            pass
    def printDetails(cls):
        print "udi=%s"%cls.__udi
        for k,v in cls.__property.items():
            print "  %s : %s"%(k,v)
        print "done!"

    def getVendor(cls):
        return cls.__vendor
    def getType(cls):
        return cls.__type
    def getUDI(cls):
        return cls.__udi
    def getDriver(cls):
        return cls.__driver
    def getSon(cls):
        return cls.__son
    def getParent(cls):
        return cls.__parent
    def getProperties(cls):
        return cls.__properties
    def translateID(cls):
        '''translate vendor & device id number into string'''
        pass
