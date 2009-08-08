#define	DRIVER_ALIAS	"/etc/driver_aliases"
#define	DRIVER_CLASSES	"/etc/driver_classes"
#define	NAM_TO_MAJ	"/etc/name_to_major"
#define	DEV_POLICY	"/etc/security/device_policy"
#define	EXTRA_PRIVS	"/etc/security/extra_privs"

1 printf priv_getbynum()
2 printf priv_getbyname()
3  char* c = priv_gettext()
   printf c
   free(c)
