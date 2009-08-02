int
main(int argc, char *argv[])
{
	char *basedir = NULL, *driver_name = NULL;
	int mod_unloaded = 0;
	int modid, found;
	int cleanup = 0;
	
	if (getopt(argc, argv, "C") == 'C') cleanup = 1;

	if (argv[optind] != NULL) (void) driver_name = argv[optind];

	if (n_flag == 0 && !server) {
		mod_unloaded = 1;

		/* module is installed */
		if (modid != -1) {
			if (modctl(MODUNLOAD, modid) < 0) {
				mod_unloaded = 0;
			}
		}
		/* unload driver.conf file */
		modctl(MODUNLOADDRVCONF, (major_t)found);
	}

	if (mod_unloaded && (modctl(MODREMMAJBIND, (major_t)found) < 0)) {
		perror(NULL);
		(void) fprintf(stderr, gettext(ERR_MODREMMAJ), found);
	}
	
	/*
	 * If removing the driver from the running system, notify
	 * kernel dynamically to remove minor perm entries.
	 */
	if ((n_flag == 0) && (basedir == NULL || (strcmp(basedir, "/") == 0))) devfs_rm_minor_perm(driver_name, log_minorperm_error);

	/*
	 * Optionally clean up any dangling devfs shadow nodes for
	 * this driver so that, in the event the driver is re-added
	 * to the system, newly created nodes won't incorrectly
	 * pick up these stale shadow node permissions.
	 */
	if ((n_flag == 0) && cleanup) 
		if ((basedir == NULL || (strcmp(basedir, "/") == 0))) {
			modctl(MODREMDRVCLEANUP, driver_name, 0, NULL);
		} 

}