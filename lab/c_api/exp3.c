/*
 * Copyright 1994-2004 Sun Microsystems, Inc.
 * All Rights Reserved.
 */


/*
 * Print all device configuration information on the system
 */

#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#include <sys/mkdev.h>
#include <sys/param.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <devid.h>
#include <libdevinfo.h>

/*
 * local data
 */
static char *progname;
static char *usage = "%s [ -p ]\n";
static int promprops = 0;       /* switch for prom properties */

/*
 * function declarations
 */
extern void exit();

static void setprogname(char *name);
static void dump_devinfo();
static int dump_node(di_node_t node, void *arg);
static void dump_prop_list(di_node_t node);
static void dump_prom_prop_list(di_node_t node, di_prom_handle_t ph);
static int dump_minor_node(di_node_t node, di_minor_t minor, void *arg);

/*
 * Formatting functions
 */
static void indent(int);
static void prt_strings(int, char *);
static void prt_nodeid(di_node_t);
static void prt_devid(di_node_t);
static void prt_driver_ops(di_node_t);
static void prt_devt(dev_t);
static char *prop_type_str(di_prop_t);
static int prop_type_guess(uchar_t *, int);

int
main(int argc, char *argv[])
{
        int     c;
        extern void exit();

        setprogname(argv[0]);
        while ((c = getopt(argc, argv, "p")) != -1)  {
                switch (c)  {
                case 'p':
                        ++promprops;
                        break;
                default:
                        (void) fprintf(stderr, usage, progname);
                        exit(1);
                }
        }

        dump_devinfo();
        return 0;
} /* main */



static void
setprogname(name)
char *name;
{
        char *p;

        if (p = strrchr(name, '/'))
                progname = p + 1;
        else
                progname = name;
}

/*
 * Call most libdevinfo public interfaces and print results
 */
static void
dump_devinfo(void)
{
        di_node_t root_node;
        di_prom_handle_t ph;

        /*
         * Snapshot with all information
         */
        if((root_node = di_init("/", DINFOCPYALL)) == DI_NODE_NIL) {
                perror("di_init() failed");
                exit(1);
        }

        /*
         * Create handle to PROM
         */
        if(promprops && (ph = di_prom_init()) == DI_PROM_HANDLE_NIL) {
                perror("di_prom_init() failed");
                di_fini(root_node);
                exit (1);
        }

        /*
         * Walk all nodes and report information in readable format
         */
        di_walk_node(root_node, DI_WALK_CLDFIRST, ph, dump_node);

        /*
         * Clean up handles
         */
        if (promprops)
                di_prom_fini(ph);

        di_fini(root_node);
}

/*
 * print out information about this node, returns appropriate code.
 * arg is used to pass the handle to PROM
 */
static int
dump_node(di_node_t node, void *arg)
{
        int i;
        char *name;
        di_prom_handle_t ph = (di_prom_handle_t)arg;

        /*
         * print physical path, no indentation
         */
        name = di_devfs_path(node);
        (void) printf("%s\n", name);
        di_devfs_path_free(name);

        /*
         * Print attributes with indentation
         */
        indent(1);
        (void) printf("compatible names: ");
        i = di_compatible_names(node, &name);
        prt_strings(i, name);

        indent(1);
        (void) printf("binding name: ");
        prt_strings(1, di_binding_name(node));

        indent(1);
        (void) printf("driver name: ");
        prt_strings(1, di_driver_name(node));

        prt_driver_ops(node);
        prt_nodeid(node);
        prt_devid(node);

        /*
         * Print properties
         */
        dump_prop_list(node);

        if (promprops)
                dump_prom_prop_list(node, ph);

        /*
         * Print minor node information
         */
        indent(1);
        (void) printf("Minor nodes:\n");
        if(di_minor_next(node, DI_MINOR_NIL) == DI_MINOR_NIL) {
                indent(2);
                (void) printf("none\n");
        } else {
                /*
                 * Print minor nodes attached to this node
                 *
                 * Note, normally di_walk_minor() visit all minor nodes
                 * in the subtree. A trick is used here to walk only
                 * those minor node exported by the current node.
                 */
                (void) di_walk_minor(node, NULL, 0,
                        (void *)node, dump_minor_node);
        }

        return (DI_WALK_CONTINUE);
}
 
/*
 * Print properties associated with node
 */
static void
dump_prop_list(di_node_t node)
{
        int rval, i, type;
        di_prop_t prop, next;
        int *intp;
        char *strp;
        uchar_t *bytep;

        indent(1);
        (void) printf("Properties:\n");

        if((next = di_prop_next(node, DI_PROP_NIL)) == DI_PROP_NIL) {
                indent(2);
                (void) printf("none\n");
                return;
        }

        while (next != DI_PROP_NIL) {
                prop = next;
                next = di_prop_next(node, prop);
                
                indent(2);
                (void) printf("name=%s, ", di_prop_name(prop));
                prt_devt(di_prop_devt(prop));
                (void) printf(", type=%s\n", prop_type_str(prop));

                indent(2);
                (void) printf("value=");

                type = di_prop_type(prop);
                if (type == DI_PROP_TYPE_UNKNOWN) {
                        rval = di_prop_bytes(prop, &bytep);
                        type = prop_type_guess(bytep, rval);
                }

                switch (type) {
                case DI_PROP_TYPE_UNDEF_IT:
                        (void) printf(" undefined.");
                        break;
                case DI_PROP_TYPE_BOOLEAN:
                        (void) printf(" true.");
                        break;
                case DI_PROP_TYPE_INT:
                        rval = di_prop_ints(prop, &intp);
                        if (rval == -1) {
                                perror("di_prop_ints");
                                break;
                        }
                        for (i = 0; i < rval; ++i)
                                (void) printf(" %d", intp[i]);
                        break;
                case DI_PROP_TYPE_STRING:
                        rval = di_prop_strings(prop, &strp);
                        if (rval == -1) {
                                perror("di_prop_strings");
                                break;
                        }
                        for (i = 0; i < rval; ++i)  {
                                (void) printf(" %s", strp);
                                strp += strlen(strp) + 1;
                        }
                        break;
                case DI_PROP_TYPE_BYTE:
                        rval = di_prop_bytes(prop, &bytep);
                        if (rval == -1) {
                                perror("di_prop_bytes");
                                break;
                        }
                        (void) printf("0x");
                        for (i = 0; i < rval; ++i)  {
                                unsigned byte;
                                byte = (unsigned)bytep[i];
                                (void) printf("%2.2x", byte);
                        }
                        break;
                default:
                        (void) fprintf(stderr,
                            " Error: unknown property type\n");
                }
                (void) printf("\n");
        }
}

/*
 * Print PROM properties attached to node.
 * PROM properties are not typed
 */
static void
dump_prom_prop_list(di_node_t node, di_prom_handle_t ph)
{
        int rval, i, type;
        di_prom_prop_t prop;
        int *intp;
        char *strp;
        uchar_t *bytep;

        indent(1);
        (void) printf("PROM properties:\n");

        if((prop = di_prom_prop_next(ph, node, DI_PROM_PROP_NIL))
            == DI_PROM_PROP_NIL) {
                indent(2);
                (void) printf("none\n");
                return;
        }

        while (prop != DI_PROM_PROP_NIL) {
                
                rval = di_prom_prop_data(prop, &bytep);
                /*
                 * Try to guess a type so the value is more readable
                 */
                type = prop_type_guess(bytep, rval);

                indent(2);
                (void) printf("%s:", di_prom_prop_name(prop));

                switch (type) {
                case DI_PROP_TYPE_BOOLEAN:
                        (void) printf(" true.");
                        break;
                case DI_PROP_TYPE_INT:
                        /*
                         * lookup interfaces provide decoding (byte-order)
                         */
                        rval = di_prom_prop_lookup_ints(ph, node,
                                di_prom_prop_name(prop), &intp);
                        if (rval == -1) {
                                perror("di_prom_prop_lookup_ints");
                                break;
                        }
                        for (i = 0; i < rval; ++i)
                                (void) printf(" %d", intp[i]);
                        break;
                case DI_PROP_TYPE_STRING:
                        rval = di_prom_prop_lookup_strings(ph, node,
                                di_prom_prop_name(prop), &strp);
                        if (rval == -1) {
                                perror("di_prom_prop_lookup_strings");
                                break;
                        }
                        for (i = 0; i < rval; ++i)  {
                                (void) printf(" %s", strp);
                                strp += strlen(strp) + 1;
                        }
                        break;
                case DI_PROP_TYPE_BYTE:
                        rval = di_prom_prop_lookup_bytes(ph, node,
                                di_prom_prop_name(prop), &bytep);
                        if (rval == -1) {
                                perror("di_prom_prop_lookup_bytes");
                                break;
                        }
                        (void) printf("0x");
                        for (i = 0; i < rval; ++i)  {
                                unsigned byte;
                                byte = (unsigned)bytep[i];
                                (void) printf("%2.2x", byte);
                        }
                        break;
                default:
                        (void) fprintf(stderr,
                            "Error: unexpected type in dump_prom_prop_list\n");
                }
                (void) printf("\n");
                prop = di_prom_prop_next(ph, node, prop);
        }
}

/*
 * Print minor nodes attached to a single device node.
 * Terminate walk when the device node changes
 */
static int
dump_minor_node(di_node_t node, di_minor_t minor, void *arg)
{
        char *type;

        if ((caddr_t)node != (caddr_t)arg)
                return (DI_WALK_TERMINATE);

        indent(2);
        (void) printf("name=%s, ", di_minor_name(minor));

        prt_devt(di_minor_devt(minor));

        type = (di_minor_spectype(minor) == S_IFCHR) ? "char" : "block";
        (void) printf(", spectype=%s, ", type);

        type = di_minor_nodetype(minor);
        if (type)
                (void) printf("nodetype=%s\n", type);
        else
                (void) printf("nodetype=NULL\n");

        return (DI_WALK_CONTINUE);
}

static void
prt_strings(int n, char *strs)
{
        if ((n == 0) || (strs == NULL)) {
                (void) printf("none\n");
                return;
        }

        if (n == 1) {
                (void) printf("%s\n", strs);
                return;
        }

        while (n) {
                (void) printf(" %s", strs);
                strs += strlen(strs) + 1;
                n--;
        }
        (void) printf("\\n");
}

static void
prt_nodeid(di_node_t node)
{
        indent(1);
        (void) printf("nodeid: ");

        switch (di_nodeid(node)) {
        case DI_PROM_NODEID:
                (void) printf("DI_PROM_NODEID\n");
                break;
        case DI_SID_NODEID:
                (void) printf("DI_SID_NODEID\n");
                break;
        case DI_PSEUDO_NODEID:
                (void) printf("DI_PSEUDO_NODEID\n");
                break;
        default:
                (void) printf("unknown\n");
        }
}

static void
prt_driver_ops(di_node_t node)
{
        uint_t ops = di_driver_ops(node);

        indent(1);
        (void) printf("driver ops: ");

        if (ops == 0) {
                (void) printf("none\n");
                return;
        }

        if (ops & DI_BUS_OPS) {
                (void) printf("DI_BUS_OPS ");
        }
        if (ops & DI_CB_OPS) {
                (void) printf("DI_CB_OPS ");
        }
        if (ops & DI_STREAM_OPS) {
                (void) printf("DI_STREAM_OPS");
        }
        (void) printf("\n");
}

static void
prt_devid(di_node_t node)
{
        int i, len;
        ddi_devid_t devid = di_devid(node);
        struct impl_devid *id = (struct impl_devid *)devid;

        indent(1);
        (void) printf("device id: ");
        if (id == NULL) {
                (void) printf("none\n");
                return;
        }

        (void) printf(" magic 0x%2.2x%2.2x",
            id->did_magic_hi, id->did_magic_lo);
        (void) printf(" revision 0x%2.2x%2.2x", id->did_rev_hi, id->did_rev_lo);
        (void) printf(" type 0x%2.2x%2.2x", id->did_type_hi, id->did_type_lo);
        (void) printf(" len 0x%2.2x%2.2x\n", id->did_len_hi, id->did_len_lo);
        indent(1);
        (void) printf("    hint ");
        for(i = 0; (i < DEVID_HINT_SIZE) && id->did_driver[i]; i++)
                (void) putchar(id->did_driver[i]);

        (void) printf(" id 0x");
        len = (id->did_len_hi << 8) + id->did_len_lo;
        for(i = 0; i < len; i++)
                (void) printf("%2.2x", id->did_id[i]);
        (void) putchar('n');
}

static void
prt_devt(dev_t dev)
{
        if (dev == DDI_DEV_T_NONE) {
                (void) printf("dev=NONE");
        } else {
                (void) printf("dev=(%ld/%ld)", major(dev), minor(dev));
        }
}

static char *
prop_type_str(di_prop_t prop)
{
        switch (di_prop_type(prop)) {
        case DI_PROP_TYPE_UNDEF_IT:
                return ("UNDEF");
        case DI_PROP_TYPE_BOOLEAN:
                return ("BOOL");
        case DI_PROP_TYPE_INT:
                return ("INT");
        case DI_PROP_TYPE_STRING:
                return ("STRING");
        case DI_PROP_TYPE_BYTE:
                return ("BYTE");
        default:
                return ("UNKNOW\n");
        }
        /* NOTREACHED */
}

/*
 * The guessing algorithm is:
 *      1. If every byte is printable, then its a string property
 *      2. Otherwise, if length is multiple of 4, its an interger property
 *      3. Otherwise, it's a byte array.
 */
static int
prop_type_guess(uchar_t *data, int len)
{
        int i, c, slen, guess;

        if (len < 0)
                return (-1);
        else if (len == 0)
                return (DI_PROP_TYPE_BOOLEAN);

        slen = 0;
        guess = DI_PROP_TYPE_STRING;

        for (i = 0; i < len; i++) {
                c = (int)data[i];
                switch (c) {
                case 0: /* null character */
                        if (slen == 0)
                                guess = DI_PROP_TYPE_BYTE;
                        else
                                slen = 0;
                        break;
                default:
                        if (! isprint(c))
                                guess = DI_PROP_TYPE_BYTE;
                        else
                                slen++;
                }

                if (guess != DI_PROP_TYPE_STRING)
                        break;
        }
                
        if ((guess == DI_PROP_TYPE_BYTE) && (len % sizeof(int) == 0))
                guess = DI_PROP_TYPE_INT;

        return (guess);
}

static void
indent(int n)
{
        const char *indent_string = "    ";

        while (n--) {
                (void) printf("%s", indent_string);
        }
}

