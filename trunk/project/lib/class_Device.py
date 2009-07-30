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
    def __init__(cls):
        pass
    def getVendor(cls):
        return cls.__vendor
    def getType(cls):
        return cls.__type
    def getPath(cls):
        return cls.__path
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
