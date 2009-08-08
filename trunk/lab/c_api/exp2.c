/*
 * Copyright 1994-2004 Sun Microsystems, Inc.
 * All Rights Reserved.
 */

/*
 * Print physical path to disk nodes bound to the sd driver
 */
#include <stdio.h>
#include <libdevinfo.h>

#define DISK_DRIVER "ide"

static void
prt_diskinfo(di_node_t node)
{
    int instance;
    char *phys_path;

    /*
     * If the device node exports no minor nodes,
     * there is no physical device.
     */
    if (di_minor_next(node, DI_MINOR_NIL) == DI_MINOR_NIL) {
        return;
    }

    instance = di_instance(node);
    phys_path = di_devfs_path(node);
    (void) printf("%s%d: %s\n", DISK_DRIVER, instance, phys_path);
    di_devfs_path_free(phys_path);
}

static void
walk_disknodes(di_node_t node)
{
    node = di_drv_first_node(DISK_DRIVER, node);
    while (node != DI_NODE_NIL) {
        prt_diskinfo(node);
        node = di_drv_next_node(node);
    }
}

int
main(void)
{
    di_node_t root_node;
    extern void exit();

    if ((root_node = di_init("/", DINFOCPYALL)) == DI_NODE_NIL) {
        perror("di_init() failed");
        exit(1);
    }
    walk_disknodes(root_node);
    di_fini(root_node);
    return 0;
}
