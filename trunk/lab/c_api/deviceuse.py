import devicec
list = devicec.get_device_info()
for item in list:
    print item
#    for (key,value) in item.items():
#        print key,'->',value
drvname = raw_input('input driver name:')
print devicec.is_device_bydrv(drvname)
print devicec.get_device_bydrv(drvname)
