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
    properties'''

    SERVICE='org.freedesktop.Hal'
    INTERFACE='org.freedesktop.Hal.Device'

    def __init__(cls, udi, property_=None):
        cls.__udi=udi
        cls.__children=[]

        if property_==None:
            cls.__property={}
        else:
            cls.__property=property_
        try:
            for k,v in cls.__property.items():
                if 'dbus.Array' in str(type(v)):
                    if v!=[]:
                        cls.__property[k]=v[0]
                    else:
                        v=None
        except:
            pass

        if property_.has_key("info.parent"):
            cls.__parent=str(property_["info.parent"])
        elif property_["info.product"]=='Computer':
            cls.__parent=""

        if property_.has_key("info.product"):
            cls.__product=str(property_["info.product"])
            #print "  [PRODUCT]",cls.__product
	else:
	    cls.__product="unknown"

        if property_.has_key("info.udi"):
            cls.__udi=property_["info.udi"]
            #print "  [UDI]",cls.__udi

        if property_.has_key("info.vendor"):
            cls.__vendor=property_["info.vendor"]
        else:
            cls.__vendor="unknown"


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
        print "    detail of udi=%s"%cls.__udi
        for k,v in cls.__property.items():
            print "       %s : %s"%(k,v)
    def printBrief(cls):
        print "udi=%s"%cls.__udi
        print "    product",cls.__product
        print "    vendor",cls.__vendor

    def getParent(cls):
        return cls.__parent

    def getVendor(cls):
        return cls.__vendor

    def getType(cls):
        return cls.__type

    def getProduct(cls):
        return cls.__product

    def getUDI(cls):
        return cls.__udi

    def getDriver(cls):
        return cls.__driver

    def getChildren(cls):
        return cls.__children

    def hasChildren(cls):
        return cls.__children!=[]

    def appendChildren(cls, child):
        cls.__children.append(child)

    def getParent(cls):
        return cls.__parent
    def getProperties(cls):
        return cls.__property

    def printTree(cls, space):
        print space,
        print "[%s]"%(cls.__product)

        for d in cls.__children:
            d.printTree("    "+space)
