static int exec_devfsadm = devfsadm -b [-c classes] -i drivername -m major_num [ -u -f -a]
int unconfig_driver(char *driver_name,major_t major_num,char *aliases,int verbose_flag,int force_flag)
	devfsadm(driver_name, major_num,aliases, NULL, verbose_flag, force_flag);
int config_driver(char *driver_name,major_t major_num,char *aliases,char *classes,int cleanup_flag,int verbose_flag)
	devfsadm(B_TRUE, driver_name, major_num,aliases, classes, verbose_flag, 0);
	if (error) remove_entry(cleanup_flag, driver_name);
void load_driver(char *driver_name, int verbose_flag)
	devfsadm [-v] -i driver_name
int check_name_to_major(int mode)
	error = (access(name_to_major,mode) != 0)
int create_reconfigure_file
	return fopen("/reconfigure","a");
#define	MOD_SEP	" :"
#define	KERNEL_DRV	"/kernel/drv"
#define	USR_KERNEL_DRV	"/usr/kernel/drv"
#define	DEVFSADM_PATH	"/usr/sbin/devfsadm"
#define	DEVFSADM	"devfsadm"
#define	DEVFS_ROOT	"/devices"
#define	RECONFIGURE	"/reconfigure"
#define	MODUNLOAD_PATH	"/usr/sbin/modunload"
#define	DRIVER_ALIAS	"/etc/driver_aliases"
#define	DRIVER_CLASSES	"/etc/driver_classes"
#define	NAM_TO_MAJ	"/etc/name_to_major"
#define	DEV_POLICY	"/etc/security/device_policy"
#define	EXTRA_PRIVS	"/etc/security/extra_privs"

1 print priv_getbynum()
2 print priv_getbyname()
3 char* c = priv_gettext()
   print c
   free(c)
