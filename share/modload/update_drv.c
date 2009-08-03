/*
 * CDDL HEADER START
 *
 * The contents of this file are subject to the terms of the
 * Common Development and Distribution License (the "License").
 * You may not use this file except in compliance with the License.
 *
 * You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
 * or http://www.opensolaris.org/os/licensing.
 * See the License for the specific language governing permissions
 * and limitations under the License.
 *
 * When distributing Covered Code, include this CDDL HEADER in each
 * file and include the License file at usr/src/OPENSOLARIS.LICENSE.
 * If applicable, add the following below this CDDL HEADER, with the
 * fields enclosed by brackets "[]" replaced with your own identifying
 * information: Portions Copyright [yyyy] [name of copyright owner]
 *
 * CDDL HEADER END
 */
/*
 * Copyright 2009 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */


/*
 * try to modunload driver.
 * return -1 on failure and 0 on success
 */
static int
unload_drv(char *driver_name, int force_flag, int verbose_flag)
{
	int modid;
	get_modid(driver_name, &modid);
	if (modid != -1) modctl(MODUNLOAD, modid) < 0)
}

int
main(int argc, char *argv[])
{
	int	major;
	int	cleanup_flag = 0;
	int	update_conf = 1;	/* reload driver.conf by default */
	int	verbose_flag = 0;	/* -v option */
	int	a_flag = 0;		/* -a option */
	int	d_flag = 0;		/* -d option */
	int	i_flag = 0;		/* -i option */
	int	l_flag = 0;		/* -l option */
	int	m_flag = 0;		/* -m option */
	char	*basedir = NULL;
	char	*driver_name;
	int	found;
	major_t major_num;
	int	rval;

	while ((opt = getopt(argc, argv, "m:ni:b:p:adlfuvP:")) != EOF) {
		switch (opt) {
		case 'a':
			a_flag++;
			break;
		case 'd':
			d_flag++;
			break;
		case 'l':	/* private option */
			l_flag++;
			break;
		}
	}

	driver_name = argv[optind];

	/*
	 * ADD: -a option
	 * i_flag: update /etc/driver_aliases
	 * m_flag: update /etc/minor_perm
	 * -p: update /etc/security/device_policy
	 * -P: update /etc/security/extra_privs
	 * if force_flag is specified continue w/ the next operation
	 */
	if (a_flag) {
		if (i_flag) {
			found = get_major_no(driver_name, name_to_major);
			major_num = (major_t)found;

			/*
			 * if the list of aliases to be added is
			 * now empty, we're done.
			 */
			if (aliases2 == NULL)
				goto done;

			/* optionally update the running system - not -b */
			if (update_conf) {
				/* paranoia - if we crash whilst configuring */
				sync();
				config_driver(driver_name, major_num,aliases2, NULL, cleanup_flag,verbose_flag);
			}

		}

done:
		if (update_conf && (i_flag || policy != NULL)) {
			/* load the driver */
			load_driver(driver_name, verbose_flag);
		}
	}


	/*
	 * DELETE: -d option
	 * i_flag: update /etc/driver_aliases
	 * m_flag: update /etc/minor_perm
	 * -p: update /etc/security/device_policy
	 * -P: update /etc/security/extra_privs
	 */
	if (d_flag) {
		if (i_flag) {
			major_num = (major_t)found;

			/*
			 * optionally update the running system - not -b.
			 * Unless -f is specified, error if one or more
			 * devices remain bound to the alias.
			 */
			if (update_conf) {
				/* paranoia - if we crash whilst configuring */
				sync();
				unconfig_driver(driver_name, major_num,aliases, verbose_flag, force_flag);
			}
		}

		if (update_conf) {
			if (i_flag || m_flag) {
				/* try to unload the driver */
				(void) unload_drv(driver_name,force_flag, verbose_flag);
			}
			/* reload the policy */
			if (policy != NULL) load_driver(driver_name, verbose_flag);
		}
	}

	/*
	 * Update driver.conf file:
	 *	First try to unload driver module. If it fails, there may
	 *	be attached devices using the old driver.conf properties,
	 *	so we cannot safely update driver.conf
	 *
	 *	The user may specify -f to force a driver.conf update.
	 *	In this case, we will update driver.conf cache. All attached
	 *	devices still reference old driver.conf properties, including
	 *	driver global properties. Devices attached in the future will
	 *	referent properties in the updated driver.conf file.
	 */
	if (update_conf) {
		unload_drv(driver_name, force_flag, verbose_flag);
		modctl(MODUNLOADDRVCONF, major);
	    modctl(MODLOADDRVCONF, major);
		load_driver(driver_name, verbose_flag);
	}
}
