"""This file contains global constants."""

NAME = "hal-device-manager"
NAME_LONG = "HAL Device Manager"
VERSION = "0.5.9"
COPYRIGHT = "Copyright (C) 2003 David Zeuthen."
INFO = "This application shows information about\nhardware on your system"""
AUTHORS = [
    "David Zeuthen <david@fubar.dk>",
    "Shannon -jj Behrens <jjinux@yahoo.com> (for simplepy)"
]

DATADIR = "/usr/share/hal/device-manager"

PIXBUF_COLUMN = 0
TITLE_COLUMN  = 1
UDI_COLUMN    = 2

BUS_NAMES = {"unknown"       : "Unknown",
             "usb_device"    : "USB",
             "platform"      : "Legacy Device",
             "usb"           : "USB Interface",
             "pci"           : "PCI",
             "i2c"           : "I2C",
             "i2c_adapter"   : "I2C Adapter",
             "video4linux"   : "Video4Linux",
             "scsi_host"     : "SCSI Host",
             "scsi"          : "SCSI",
             "block"         : "Block",
             "ide"           : "IDE",
             "pnp"           : "PNP",
             "ide_host"      : "IDE Host",
             "macio"         : "MacIO",
             "serio"         : "serio",
             "ieee1394"      : "IEEE1394",
             "serial"        : "Serial",
             "usb-serial"    : "USB Serial",
             "pcmcia"        : "PCMCIA"}

STATE_NAMES = { 0 : "No device information file was found",
                1 : "Enabling...",
                2 : "Need information to enable",
                3 : "Error enabling the device",
                4 : "Enabled",
                5 : "Disabling...",
                6 : "Disabled",
                7 : "Not plugged in" }

