'''this class is the definition of class: Device
created @ 09.07.27 by 韩志超'''

class Device(object):
    '''class of Device'''
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
