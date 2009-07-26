/*
 * Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */

#ifndef	_DMI_INFO_H
#define	_DMI_INFO_H

#pragma ident	"@(#)dmi_info.h	1.3	09/04/28 SMI"

#ifdef __cplusplus
extern "C" {
#endif

#define	u8			unsigned char
#define	PRINTF			(void) printf
#define	NODE_PLATFORM		"platform"
#define	CLASS_PROM		"openprom"
#define	CLASS_CPU		"cpu"
#define	CLASS_MEMBANK		"memory-bank"

static const char *system_prop[] = {
	"PlatformGroup",
	"banner-name",
	"model",
	NULL
};

static const char *system_info[] = {
	"PlatformGroup",
	"Product",
	"Model",
	NULL
};

static const char *prom_prop[] = {
	"model",
	"version",
	NULL
};

static const char *prom_info[] = {
	"Model",
	"Version",
	NULL
};

static const char *processor_prop[] = {
	"name",
	"ProcessorType",
	"FPUType",
	"sparc-version",
	"clock-frequency",
	"State",
	"portid",
	"cpuid",
	"ecache-size",
	"icache-size",
	"dcache-size",
	NULL
};

static const char *processor_name[] = {
	"Processor Name",
	"Processor Type",
	"FPU Type",
	"Sparc Version",
	"Clock Frequency",
	"State",
	"PortID",
	"CPUID",
	"ecache-size",
	"icache-size",
	"dcache-size",
	NULL
};

static const char *cpu_prop[] = {
	"name",
	NULL
};

static const char *cpu_info[] = {
	"CPU Type",
	NULL
};

static const char *mem_prop[] = {
	"ID",
	"Size",
	NULL
};

static const char *mem_info[] = {
	"Memory Device Locator",
	"Memory Size",
	NULL
};

typedef struct virtual_cpu_info {
	int	chip_id;
	int	core_id;
} *virtual_cpu_info_t;

typedef struct processor_pkg_info {
	int	pkg_id;
	int	cpu_id;
	char 	*brand;
	int	num_core;
	int	num_thread;
	struct processor_pkg_info	*next;
} *processor_pkg_info_t;

#ifdef __cplusplus
}
#endif

#endif /* _DMI_INFO_H */
