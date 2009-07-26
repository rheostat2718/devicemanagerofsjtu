"""This file contains the DeviceManager class."""
 
import sys
import dbus
if getattr(dbus, "version", (0,0,0)) >= (0,41,0):
    import dbus.glib
 
class DeviceManager(LibGladeApplication):
    """This is the main window for the application."""

    SERVICE='org.freedesktop.Hal'
    OBJECT='/org/freedesktop/Hal/Manager'
    INTERFACE='org.freedesktop.Hal.Manager'
    
    def __init__(self):
        """Connect to the HAL daemon."""

        ver = getattr(dbus, 'version', (0, 0, 0))
        if ver < (0, 40, 0):
            self.warn('Your version of DBUS is too low!')
            exit(1)

        self.bus = dbus.SystemBus()
        self.hal_manager_obj = self.bus.get_object(DeviceManager.SERVICE,DeviceManager.OBJECT)
        self.hal_manager = dbus.Interface(self.hal_manager_obj,DeviceManager.INTERFACE)

        # gdl_changed will be invoked when the Global Device List is changed
        # per the hal spec
        self.hal_manager.connect_to_signal("DeviceAdded", 
                         lambda *args: self.gdl_changed("DeviceAdded", *args))
        self.hal_manager.connect_to_signal("DeviceRemoved", 
                         lambda *args: self.gdl_changed("DeviceRemoved", *args))
        self.hal_manager.connect_to_signal("NewCapability", 
                         lambda *args: self.gdl_changed("NewCapability", *args))

        # Add listeners for all devices
        try:
            device_names = self.hal_manager.GetAllDevices()
        except:
            self.warn("Can't get all device information")
            sys.exit(1)
        for name in device_names:
	    self.add_device_signal_recv (name);

    def add_device_signal_recv (self, udi):
	self.bus.add_signal_receiver(lambda *args: self.property_modified(udi, *args),
				     "PropertyModified",
				     "org.freedesktop.Hal.Device",
				     "org.freedesktop.Hal",
				     udi)

    def remove_device_signal_recv (self, udi):
        try:
            self.bus.remove_signal_receiver(None,
				            "PropertyModified",
				            "org.freedesktop.Hal.Device",
				            "org.freedesktop.Hal",
				            udi)
        except Exception, e:
            print "Older versions of the D-BUS bindings have an error when removing signals. Please upgrade."
            print e

    def device_condition(self, device_udi, condition_name, condition_details):
        """This method is called when signals on the Device interface is
        received"""

	print "\nCondition device=%s"%device_udi
	print "  (condition_name, condition_details) = ('%s', '%s')"%(condition_name, condition_details)

    def gdl_changed(self, signal_name, device_udi, *args):
        """This method is called when a HAL device is added or removed."""

        if signal_name=="DeviceAdded":
            print "\nDeviceAdded, udi=%s"%(device_udi)
	    self.add_device_signal_recv (device_udi)
        elif signal_name=="DeviceRemoved":
            print "\nDeviceRemoved, udi=%s"%(device_udi)
	    self.remove_device_signal_recv (device_udi)
        elif signal_name=="NewCapability":
            [cap] = args 
            print "\nNewCapability, cap=%s, udi=%s"%(cap, device_udi)
        else:
            print "*** Unknown signal %s"% signal_name

