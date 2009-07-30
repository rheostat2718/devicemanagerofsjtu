/*
 * Copyright 1994-2004 Sun Microsystems, Inc.
 * All Rights Reserved.
 */

/*
 * Print node names of all device nodes
 */
#include <stdio.h>
#include <libdevinfo.h>
#include <sys/utsname.h>
/*ARGSUSED*/
static int
prt_nodename(di_node_t node, void *arg)
{
    (void) printf("%s\n", di_node_name(node));
    return (DI_WALK_CONTINUE);
}

int 
main(void)
{
    di_node_t root_node;
    extern void exit();

    if ((root_node = di_init("/", DINFOSUBTREE)) == DI_NODE_NIL) {
        perror("di_init() failed\n");
        exit(1);
    }
    /*
     * Walk device tree in child-first order and print node name
     */
    (void) di_walk_node(root_node, DI_WALK_CLDFIRST, NULL, prt_nodename);
    di_fini(root_node);
    return 0;
}
