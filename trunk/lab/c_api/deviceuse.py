import devicec
list = devicec.get_device_info()
for item in list:
    print item
#    for (key,value) in item.items():
#        print key,'->',value