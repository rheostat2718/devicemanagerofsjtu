/*
 * Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */

#pragma ident	"@(#)dmi_info.c 1.7 09/04/28 SMI"

#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include <unistd.h>
#include <picl.h>
#include <sys/processor.h>
#include <kstat.h>
#include "dmi_info.h"

int	granu;
int	cpu_num;

void
usage()
{
	PRINTF("Usage: dmi_info [ABMmPSVv]\n");
	PRINTF("       -A: print all information\n");
	PRINTF("       -B: print BIOS information \n");
	PRINTF("       -M: print Motherboard information\n");
	PRINTF("       -m: print memory subsystem information\n");
	PRINTF("       -P: print Processor information\n");
	PRINTF("       -p: print Processor number and core number\n");
	PRINTF("       -V: print SMBIOS version\n");
	PRINTF("       -v: print with verbose mode\n");
	PRINTF("       -h: for help\n");
	exit(1);
}

void
prt_prop_val(picl_prophdl_t proph, picl_propinfo_t *pinfo)
{
	int	ret;
	void 	*data;
	char 	*str;

	if (!(pinfo->accessmode & PICL_READ)) {
		return;
	}

	if (pinfo->size == 0) {
		return;
	}

	data = malloc(pinfo->size);

	if (data == NULL) {
		return;
	}

	ret = picl_get_propval(proph, data, pinfo->size);

	if (ret) {
		(void) free(data);
		return;
	}

	switch (pinfo->type) {
		case PICL_PTYPE_CHARSTRING:
			PRINTF("%s", (char *)data);
			break;

		case PICL_PTYPE_INT:
			switch (pinfo->size) {
				case sizeof (char):
					PRINTF("%d",
					*(char *)data / granu);
					break;
				case sizeof (short):
					PRINTF("%hd",
					*(short *)data / granu);
					break;
				case sizeof (int):
					PRINTF("%d",
					*(int *)data / granu);
					break;
				case sizeof (long long):
					PRINTF("%lld",
						*(long long *)data / granu);
					break;
				default:
					PRINTF("err");
			}
			break;

		case PICL_PTYPE_UNSIGNED_INT:
			switch (pinfo->size) {
				case sizeof (unsigned char):
					PRINTF("%x",
					*(unsigned char *)data / granu);
					break;
				case sizeof (unsigned short):
					PRINTF("%hx",
					*(unsigned short *)data / granu);
					break;
				case sizeof (unsigned int):
					PRINTF("%u",
					*(unsigned int *)data / granu);
					break;
				case sizeof (unsigned long long):
					PRINTF("%llu",
					*(unsigned long long *)data / granu);
					break;
				default:
					PRINTF("err");
			}
			break;

		case PICL_PTYPE_FLOAT:
			switch (pinfo->size) {
				case sizeof (float):
					PRINTF("%f", *(float *)data);
					break;
				case sizeof (double):
					PRINTF("%f", *(double *)data);
					break;
				default:
					PRINTF("err");
			}
			break;

		case PICL_PTYPE_TIMESTAMP:
			str = ctime((time_t *)data);

			if (str) {
				str[strlen(str) - 1] = '\0';
				PRINTF("%s", str);
			}
			break;

		case PICL_PTYPE_TABLE:
			PRINTF("TBL");
			break;
		case PICL_PTYPE_REFERENCE:
			PRINTF("REF");
			break;
		case PICL_PTYPE_BYTEARRAY:
			PRINTF("BIN");
			break;
		default:
			PRINTF("unknown");
	}

	(void) free(data);
}

void
prt_node_props(picl_nodehdl_t nodeh)
{
	int	ret;
	picl_prophdl_t proph;
	picl_propinfo_t pinfo;

	ret = picl_get_first_prop(nodeh, &proph);

	while (!ret) {
		ret = picl_get_propinfo(proph, &pinfo);

		if (!ret) {
			if (ret) {
				PRINTF("\t%s = ", pinfo.name);
				prt_prop_val(proph, &pinfo);
				PRINTF("\n");
			}
		}

		ret = picl_get_next_prop(proph, &proph);
	}
}

void
print_bios_info(picl_nodehdl_t  nodeh, int verbose)
{
	int		ret, i;
	picl_prophdl_t	proph;
	picl_propinfo_t	pinfo;

	if (verbose) {
		prt_node_props(nodeh);
		return;
	}

	PRINTF(" Vendor:\n");
	i = 1;

	while (prom_prop[i]) {
		if (prom_info[i]) {
			PRINTF(" %s:", prom_info[i]);
		} else {
			PRINTF(" %s:", prom_prop[i]);
		}

		ret = picl_get_propinfo_by_name(nodeh, prom_prop[i],
						&pinfo, &proph);

		if (ret == 0) {
			prt_prop_val(proph, &pinfo);
		}
		PRINTF("\n");

		i++;
	}
	PRINTF(" Release Date:\n");
	PRINTF(" BIOS Revision:\n");
	PRINTF(" Firmware Revision:\n");
}

void
print_system_info(picl_nodehdl_t  nodeh, int verbose)
{
	int		ret, i;
	picl_prophdl_t	proph;
	picl_propinfo_t	pinfo;

	if (verbose) {
		prt_node_props(nodeh);
		return;
	}

	PRINTF(" Manufacturer:SUN\n");
	i = 1;

	while (system_prop[i]) {
		if (system_info[i]) {
			PRINTF(" %s:", system_info[i]);
		} else {
			PRINTF(" %s:", system_prop[i]);
		}

		ret = picl_get_propinfo_by_name(nodeh, system_prop[i],
						&pinfo, &proph);

		if (ret == 0) {
			prt_prop_val(proph, &pinfo);
		}
		PRINTF("\n");

		i++;
	}
}

int
print_processor_info(picl_nodehdl_t nodeh, void *args)
{
	int		ret, i;
	picl_prophdl_t	proph;
	picl_propinfo_t	pinfo;

	PRINTF(" Processor %d:\n", cpu_num);
	cpu_num++;

	i = *(int *)args;

	if (i) {
		prt_node_props(nodeh);
		return (PICL_WALK_CONTINUE);
	}

	i = 0;

	while (processor_prop[i]) {
		if (processor_name[i]) {
			PRINTF("  %s: ", processor_name[i]);
		} else {
			PRINTF("  %s: ", processor_prop[i]);
		}

		ret = picl_get_propinfo_by_name(nodeh, processor_prop[i],
						&pinfo, &proph);

		if (ret == 0) {
			if (i == 4) {
				granu = 1000000;
			}

			prt_prop_val(proph, &pinfo);

			if (i == 4) {
				granu = 1;
				PRINTF("MHZ");
			}
		}
		PRINTF("\n");

		i++;
	}
	PRINTF("\n");

	return (PICL_WALK_CONTINUE);
}

void
scan_cpu_info()
{
	int			i, j, ret;
	int			npkg;
	long			nconf, nonline;
	processor_pkg_info_t	pkg_info;
	processor_pkg_info_t	info;
	processor_pkg_info_t	p;
	kstat_ctl_t		*kc;
	kstat_t			*ksp;
	kstat_named_t		*k;
	virtual_cpu_info_t	v_info;
	processor_info_t	p_info;

	nconf = sysconf(_SC_NPROCESSORS_CONF);

	if (nconf <= 0) {
		nconf = 0;
	}

	nonline = sysconf(_SC_NPROCESSORS_ONLN);

	if (nonline <= 0) {
		nonline = 0;
	}

	v_info = NULL;
	kc = kstat_open();

	if (kc) {
		v_info = (virtual_cpu_info_t)
		malloc(sizeof (struct virtual_cpu_info) * nconf);

		if (v_info == NULL) {
			(void) kstat_close(kc);
			kc = NULL;
		}
	}

	pkg_info = NULL;
	npkg = 0;

	if (kc) {
		for (i = 0; i < nconf; i++) {
			ksp = kstat_lookup(kc, "cpu_info", i, NULL);

			if (ksp == NULL) {
				break;
			}

			ret = kstat_read(kc, ksp, NULL);

			if (ret == -1) {
				break;
			}

			k = (kstat_named_t *)
				kstat_data_lookup(ksp, "chip_id");

			if (k == NULL) {
				break;
			}

			v_info[i].chip_id = k->value.i32;

			k = (kstat_named_t *)
				kstat_data_lookup(ksp, "core_id");

			if (k == NULL) {
				break;
			}

			v_info[i].core_id = k->value.i32;

			info = pkg_info;

			while (info) {
				if (info->pkg_id == v_info[i].chip_id) {
					break;
				} else {
					info = info->next;
				}
			}

			if (info == NULL) {
				info = (processor_pkg_info_t)
				malloc(sizeof (struct processor_pkg_info));

				if (info == NULL) {
					break;
				}

				info->pkg_id = v_info[i].chip_id;
				info->cpu_id = i;
				info->num_core = 0;
				info->num_thread = 0;
				info->brand = NULL;
				info->next = NULL;

				k = (kstat_named_t *)
				kstat_data_lookup(ksp, "brand");

				if (k) {
					info->brand = k->value.str.addr.ptr;
				}

				if (pkg_info) {
					p = pkg_info;
					while (p->next) {
						p = p->next;
					}
					p->next = info;
				} else {
					pkg_info = info;
				}

				npkg++;
			}

			info->num_thread++;

			for (j = 0; j < i; j++) {
				if ((v_info[j].chip_id == v_info[i].chip_id) &&
				(v_info[j].core_id == v_info[i].core_id))
				break;
			}

			if (j >= i) {
				info->num_core++;
			}
		}
		(void) free(v_info);
	} else {
		npkg = nconf;
	}

	if (pkg_info && pkg_info->brand) {
		PRINTF("CPU Type:%s", pkg_info->brand);
	} else {
		PRINTF("CPU Type:cpu");
	}

	ret = processor_info(info->cpu_id, &p_info);

	if (ret) {
		PRINTF("\n");
	} else {
		PRINTF(",%s\n", p_info.pi_processor_type);
	}

	if (pkg_info) {
		PRINTF("CPU Number:%d\n", npkg);
		PRINTF("Number of cores per processor:%d\n",
			pkg_info->num_core);
		PRINTF("Number of threads per processor:%d\n",
			pkg_info->num_thread);
	} else {
		PRINTF("CPU Number:%ld\n", nconf);
		PRINTF("Number of cores per processor:1\n");
		PRINTF("Number of threads per processor:1\n");
	}


	while (pkg_info) {
		info = pkg_info;
		pkg_info = pkg_info->next;
		(void) free(info);
	}

	if (kc) {
		(void) kstat_close(kc);
	}
}

int
print_memory_info(picl_nodehdl_t nodeh, void *args)
{
	int		ret, i;
	picl_prophdl_t	proph;
	picl_propinfo_t	pinfo;

	i = *(int *)args;

	if (i) {
		prt_node_props(nodeh);
		return (PICL_WALK_CONTINUE);
	}

	i = 0;

	while (mem_prop[i]) {
		if (mem_info[i]) {
			PRINTF(" %s: ", mem_info[i]);
		} else {
			PRINTF(" %s: ", mem_prop[i]);
		}

		ret = picl_get_propinfo_by_name(nodeh, mem_prop[i],
						&pinfo, &proph);

		if (ret == 0) {
			if (i == 1) {
				granu = 1024 * 1024;
			}
			prt_prop_val(proph, &pinfo);

			if (i == 1) {
				granu = 1;
				PRINTF("M");
			}
		}
		PRINTF("\n");

		i++;
	}
	PRINTF("\n");

	return (PICL_WALK_CONTINUE);
}

int
prt_mem_bank_size(picl_nodehdl_t nodeh, void *args)
{
	int		ret;
	void 		*data;
	u_longlong_t	value;
	unsigned long	size;
	picl_prophdl_t	proph;
	picl_propinfo_t	pinfo;
	char		c;

	ret = picl_get_propinfo_by_name(nodeh, mem_prop[1],
						&pinfo, &proph);

	if (ret) {
		return (PICL_WALK_CONTINUE);
	}

	if (!(pinfo.accessmode & PICL_READ)) {
		return (PICL_WALK_CONTINUE);
	}

	if (pinfo.size == 0) {
		return (PICL_WALK_CONTINUE);
	}

	data = malloc(pinfo.size);

	if (data == NULL) {
		return (PICL_WALK_CONTINUE);
	}

	ret = picl_get_propval(proph, data, pinfo.size);

	if (ret) {
		(void) free(data);
		return (PICL_WALK_CONTINUE);
	}

	if ((pinfo.type == PICL_PTYPE_INT) ||
	(pinfo.type == PICL_PTYPE_UNSIGNED_INT)) {
		switch (pinfo.size) {
			case sizeof (char):
				value = *(unsigned char *)data;
				break;
			case sizeof (short):
				value = *(unsigned short *)data;
				break;
			case sizeof (int):
				value =	*(unsigned int *)data;
				break;
			case sizeof (long long):
				value =	*(unsigned long long *)data;
				break;
			default:
				break;
		}
	}

	if (value == 0) {
		(void) free(data);
		return (PICL_WALK_CONTINUE);
	}

	if (*(int *)args == 0) {
		PRINTF("(");
	} else {
		PRINTF(" + ");
	}

	value = value >> 10;

	if (value >= 1024) {
		value = value >> 10;

		if (value >= 1024) {
			size = (unsigned long) (value & 0x3ff);
			value = value >> 10;
			c = 'G';
		} else {
			size = 0;
			c = 'M';
		}
	} else {
		size = 0;
		c = 'K';
	}

	if (size) {
		PRINTF("%llu.%lu%c", value, (size * 10) / 1024, c);
	} else {
		PRINTF("%llu%c", value, c);
	}

	*(int *)args = *(int *)args + 1;

	(void) free(data);
	return (PICL_WALK_CONTINUE);
}

int
get_memory_bank_size(picl_nodehdl_t nodeh, void *args)
{
	int		ret;
	void 		*data;
	picl_prophdl_t	proph;
	picl_propinfo_t	pinfo;

	ret = picl_get_propinfo_by_name(nodeh, mem_prop[1],
						&pinfo, &proph);

	if (ret) {
		return (PICL_WALK_CONTINUE);
	}

	if (!(pinfo.accessmode & PICL_READ)) {
		return (PICL_WALK_CONTINUE);
	}

	if (pinfo.size == 0) {
		return (PICL_WALK_CONTINUE);
	}

	data = malloc(pinfo.size);

	if (data == NULL) {
		return (PICL_WALK_CONTINUE);
	}

	ret = picl_get_propval(proph, data, pinfo.size);

	if (ret) {
		(void) free(data);
		return (PICL_WALK_CONTINUE);
	}

	if ((pinfo.type == PICL_PTYPE_INT) ||
	(pinfo.type == PICL_PTYPE_UNSIGNED_INT)) {
		switch (pinfo.size) {
			case sizeof (char):
				*(u_longlong_t *)args =
				*(u_longlong_t *)args +
				*(unsigned char *)data;
				break;
			case sizeof (short):
				*(u_longlong_t *)args =
				*(u_longlong_t *)args +
				*(unsigned short *)data;
				break;
			case sizeof (int):
				*(u_longlong_t *)args =
				*(u_longlong_t *)args +
				*(unsigned int *)data;
				break;
			case sizeof (long long):
				*(u_longlong_t *)args =
				*(u_longlong_t *)args +
				*(unsigned long long *)data;
				break;
			default:
				break;
		}
	}

	(void) free(data);
	return (PICL_WALK_CONTINUE);
}

u_longlong_t
get_phy_mem_size(picl_nodehdl_t nodeh)
{
	u_longlong_t	size;

	size = 0;
	(void) picl_walk_tree_by_class(nodeh, CLASS_MEMBANK, &size,
			get_memory_bank_size);

	return (size);
}

int
main(int argc, char **argv)
{
	int		c;
	int		verbose = 0;
	u8		opt_bios = 0;
	u8		opt_sys = 0;
	u8		opt_mb = 0;
	u8		opt_cpu = 0;
	u8		opt_pro = 0;
	u8		opt_mem = 0;
	u8		operate = 0;
	int		ret;
	picl_nodehdl_t  rooth;
	picl_nodehdl_t  nodeh;

	while ((c = getopt(argc, argv, "ABMmPCSv")) != EOF) {
		switch (c) {
		case 'A':
			opt_bios = 1;
			opt_sys = 1;
			opt_mb = 1;
			opt_cpu = 1;
			opt_mem = 1;
			operate++;
			break;
		case 'B':
			opt_bios = 1;
			operate++;
			break;
		case 'M':
			opt_mb = 1;
			operate++;
			break;
		case 'm':
			opt_mem = 1;
			operate++;
			break;
		case 'P':
			opt_cpu = 1;
			operate++;
			break;
		case 'C':
			opt_pro = 1;
			operate++;
			break;
		case 'S':
			opt_sys = 1;
			operate++;
			break;
		case 'v':
			verbose = 1;
			break;
		default:
			usage();
			break;
		}
	}

	if (operate == 0) {
		opt_bios = 1;
		opt_sys = 1;
		opt_mb = 1;
		opt_cpu = 1;
		opt_mem = 1;
	}

	ret = picl_initialize();

	if (ret) {
		PRINTF("error open PICL\n");
		return (1);
	}

	ret = picl_get_root(&rooth);

	if (ret) {
		PRINTF("error get root\n");
		(void) picl_shutdown();

		return (1);
	}

	granu = 1;

	if (opt_bios) {
		ret = picl_find_node(rooth, PICL_PROP_CLASSNAME,
			PICL_PTYPE_CHARSTRING,	CLASS_PROM,
			sizeof (CLASS_PROM), &nodeh);

		if (ret == 0) {
			PRINTF("BIOS Information:\n");
			print_bios_info(nodeh, verbose);
			PRINTF("\n");
		}
	}

	if (opt_sys) {
		ret = picl_find_node(rooth, PICL_PROP_NAME,
			PICL_PTYPE_CHARSTRING,	NODE_PLATFORM,
			sizeof (NODE_PLATFORM), &nodeh);

		if (ret == 0) {
			PRINTF("System Information:\n");
			print_system_info(nodeh, verbose);
			PRINTF("\n");
		}
	}


	if (opt_mb) {
		PRINTF("MotherBoard Information:\n");
		PRINTF(" Product:\n");
		PRINTF(" Manufacturer:\n");
		PRINTF(" Version:\n");
		PRINTF(" Onboard Devices:\n");
		PRINTF("\n");
	}

	if (opt_cpu) {
		PRINTF("CPU Information:\n");
		cpu_num = 0;
		(void) picl_walk_tree_by_class(rooth, CLASS_CPU, &verbose,
			print_processor_info);
	}

	if (opt_mem) {
		u_longlong_t	mem_size;
		int		item;

		PRINTF("Memory Information:\n");
		mem_size = get_phy_mem_size(rooth);

		if (mem_size) {
			mem_size = mem_size >> 10;

			if (mem_size > 1024) {
				mem_size = mem_size >> 10;

				if (mem_size > 1024) {
					PRINTF("Physical Memory: %lluG ",
						mem_size >> 10);
				} else {
					PRINTF("Physical Memory: %lluM ",
						mem_size);
				}
			} else {
				PRINTF("Physical Memory: %lluK",
						mem_size);
			}

			item = 0;
			(void) picl_walk_tree_by_class(rooth, CLASS_MEMBANK,
				&item, prt_mem_bank_size);

			if (item > 0) {
				PRINTF(")");
			}
			PRINTF("\n");
		} else {
			u_longlong_t		pages;
			u_longlong_t		pagesize;

			pagesize = sysconf(_SC_PAGESIZE);
			pages = sysconf(_SC_PHYS_PAGES);

			PRINTF("Physical Memory: %lluM\n",
				pages*pagesize >> 20);
		}

		PRINTF("\n");

		(void) picl_walk_tree_by_class(rooth, CLASS_MEMBANK, &verbose,
			print_memory_info);
	}

	if (opt_pro) {
		scan_cpu_info();
	}

	(void) picl_shutdown();
	return (0);
}
