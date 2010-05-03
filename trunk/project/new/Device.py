'''File: Device.py
data structure of device
'''

class Device(object):
    '''class for device'''
    SERVICE='org.freedesktop.Hal'
    INTERFACE='org.freedesktop.Hal.Device'

    def __init__(self, udi, property_=None):
        self.udi=udi
        self.children=[]
        self.key_info={}

        if property_==None:
            self.property_={}
        else:
            self.property_=property_

        try:
            for k,v in self.property_.items():
                if 'dbus.Array' in str(type(v)):
                    if v!=[]:
                        self.property_[k]=v[0]
                    else:
                        v=None
        except:
            pass

        if property_.has_key("info.parent"):
            self.key_info['parent']=str(property_["info.parent"])

        if property_.has_key("info.product"):
            self.key_info["product"]=str(property_["info.product"])

        if property_.has_key("info.solaris.driver"):
            self.key_info["type"]=str(property_["info.solaris.driver"])

        if property_.has_key("info.udi"):
            self.udi=property_["info.udi"]

        if property_.has_key("info.vendor"):
            self.key_info['vendor']=property_["info.vendor"]
        else:
            self.key_info["vendor"]="unknown"

    def get(self, key):
        '''get key info'''
        if self.key_info.has_key(key):
            return self.key_info[key]
        else:
            return "None"

    def get_key_info_length(self):
        '''get key info length'''
        return len(self.key_info)

    def has_children(self):
        '''check if has chilren'''
        return self.children!=[]

    def append_child(self, child):
        '''append a child'''
        self.children.append(child)

    def print_tree(self, space):
        '''print structure of device tree'''
        print space
        print "[%s]"%(self.get("product"))

        for child in self.children:
            child.print_tree("    "+space)
