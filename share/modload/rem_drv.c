char *driver_name = argv[optind];
int modid = getmodid();

/* module is installed */
if (modid != -1) modctl(MODUNLOAD, modid) //MODUNLOAD
/* unload driver.conf file */
modctl(MODUNLOADDRVCONF, (major_t)found);
//-c
modctl(MODREMDRVCLEANUP, driver_name, 0, NULL);
