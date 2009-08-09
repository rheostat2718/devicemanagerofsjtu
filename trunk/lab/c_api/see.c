#define	DRIVER_ALIAS	"/etc/driver_aliases"
#define	DRIVER_CLASSES	"/etc/driver_classes"
#define	NAM_TO_MAJ	"/etc/name_to_major"
#define	DEV_POLICY	"/etc/security/device_policy"
#define	EXTRA_PRIVS	"/etc/security/extra_privs"

useful commands:
'isainfo -b'
'uname -a'
'%s/dmi_info -C' % bindir
'/usr/sbin/prtconf -pv'
'/usr/sbin/prtdiag'
'%s/dmi_info' % bindir
