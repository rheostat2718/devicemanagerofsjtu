#include <Python.h>
#include <libdevinfo.h>
#include <stdio.h>
#include <string.h>

int walker_addtolist(di_node_t node, void *list) {
	PyObject * dict = PyDict_New();
	PyObject * compat = PyList_New(0);
	char * name = NULL;
	int count = di_compatible_names(node,&name);
	int id = di_nodeid(node);
	int state = di_node_state(node);
	int ops = di_driver_ops(node);
	PyDict_SetItem(dict, Py_BuildValue("s","name"),Py_BuildValue("s",di_node_name(node)));
	PyDict_SetItem(dict, Py_BuildValue("s","addr"),Py_BuildValue("s",di_bus_addr(node)));
	PyDict_SetItem(dict, Py_BuildValue("s","binding_name"),Py_BuildValue("s",di_binding_name(node)));
	PyDict_SetItem(dict, Py_BuildValue("s","compatible_names_no"),Py_BuildValue("i",count));
	while (count > 0) {
		PyList_Append(compat,Py_BuildValue("s",name));
		name = name+strlen(name)+1;
		count -= 1;
	}
	PyDict_SetItem(dict, Py_BuildValue("s","compatible names"),compat);
	PyDict_SetItem(dict,Py_BuildValue("s","instance"),Py_BuildValue("i",di_instance(node)));
	PyDict_SetItem(dict,Py_BuildValue("s","id"),Py_BuildValue("i",id));
	PyDict_SetItem(dict,Py_BuildValue("s","pseudo"),Py_BuildValue("i",(id & DI_PSEUDO_NODEID)));
	PyDict_SetItem(dict,Py_BuildValue("s","prom"),Py_BuildValue("i",(id & DI_PROM_NODEID)));
	//have additional properties : di_prom_prop_data di_prom_prop_lookup_bytes
	PyDict_SetItem(dict,Py_BuildValue("s","sid"),Py_BuildValue("i",(id & DI_SID_NODEID)));
	PyDict_SetItem(dict,Py_BuildValue("s","driver_major"),Py_BuildValue("i",di_driver_major(node)));
	PyDict_SetItem(dict,Py_BuildValue("s","state"),Py_BuildValue("l",di_state(node)));
	PyDict_SetItem(dict,Py_BuildValue("s","node_state"),Py_BuildValue("l",state));
	PyDict_SetItem(dict,Py_BuildValue("s","driver_detached"),Py_BuildValue("i",(state & DI_DRIVER_DETACHED)));
	PyDict_SetItem(dict,Py_BuildValue("s","device_offline"),Py_BuildValue("i",(state & DI_DEVICE_OFFLINE)));
	PyDict_SetItem(dict,Py_BuildValue("s","device_down"),Py_BuildValue("i",(state & DI_DEVICE_DOWN)));
	PyDict_SetItem(dict,Py_BuildValue("s","device_degraded"),Py_BuildValue("i",(state & DI_DEVICE_DEGRADED)));
	PyDict_SetItem(dict,Py_BuildValue("s","bus_quiesced"),Py_BuildValue("i",(state & DI_BUS_QUIESCED)));
	PyDict_SetItem(dict,Py_BuildValue("s","bus_down"),Py_BuildValue("i",(state & DI_BUS_DOWN)));
	PyDict_SetItem(dict,Py_BuildValue("s","devid"),Py_BuildValue("l",di_devid(node)));
	PyDict_SetItem(dict,Py_BuildValue("s","driver_name"),Py_BuildValue("s",di_driver_name(node)));
	PyDict_SetItem(dict,Py_BuildValue("s","driver_ops"),Py_BuildValue("l",ops));
	PyDict_SetItem(dict,Py_BuildValue("s","cb_ops"),Py_BuildValue("l",(ops & DI_CB_OPS)));
	PyDict_SetItem(dict,Py_BuildValue("s","bus_ops"),Py_BuildValue("l",(ops & DI_BUS_OPS)));
	PyDict_SetItem(dict,Py_BuildValue("s","stream_ops"),Py_BuildValue("l",(ops & DI_STREAM_OPS)));
	PyList_Append((PyObject *)list,dict);
	return (DI_WALK_CONTINUE);
}

static PyObject * get_device_info(PyObject *self) {
	di_node_t root_node;
	if ((root_node = di_init("/",DINFOSUBTREE)) == DI_NODE_NIL)
		return NULL;
	PyObject *devlist = PyList_New(0);
	(void) di_walk_node(root_node, DI_WALK_CLDFIRST,(void *)devlist,walker_addtolist);
	di_fini(root_node);
//addToList
	return devlist;
}

static struct PyMethodDef devicec_methods[] = {
		{"get_device_info",get_device_info,0},
		{NULL,NULL}};

void initdevicec() {
	(void) Py_InitModule("devicec",devicec_methods);
}

/*3
void di_node_private_set(di_node_t node,void *data);
void *di_node_private_get(di_node_t node);
void di_path_private_set(di_path_t path,void *data);
void *di_path_private_get(di_path_t path);
void di_minor_private_set(di_minor_t minor,void *data);
void *di_minor_private_get(di_minor_t minor);
void di_link_private_set(di_link_t link,void *data);
void *di_link_private_get(di_link_t link);
void di_lnode_private_set(di_lnode_t lnode,void *data);
void *di_lnode_private_get(di_lnode_t lnode);

4
char * di_devfs_path(di_node_t node);
char * di_devfs_minor_path(di_minor_t minor);
char * di_path_devfs_path(di_path_t path);
char * di_path_client_devfs_path(di_path_t path);
void * di_devfs_path_free(char *path_buf);

5
di_path_t di_path_phci_next_path(di_node_t node,di_path_t path);
di_path_t di_path_client_next_path(di_node_t node,di_path_t path);
on error:		DI_PATH_NIL
di_node_t di_path_phci_node(di_path_t path);
di_node_t di_path_client_node(di_path_t path);
char * di_path_bus_addr(di_path_t path);
int di_path_instance(di_path_t path);
path_instance:
unrelated to node_instance
persistent across attach/detach/reconfiguration , but !reboot
char * di_path_node_name(di_path_t path);
di_path_state_t di_path_state(di_path_t path);
DI_PATH_STATE_ONLINE		online, I/O requests  pass
DI_PATH_STATE_OFFLINE		offline
DI_PATH_STATE_FAULT		not ready for I/O operation
DI_PATH_STATE_STANDBY	not ready for I/O operation

6
int di_walk_minor(di_node_t root,const char* minor_nodetype,uint_t flag, void *arg, int(*minor_callback)(di_node_t node,di_minor_t minor, void *arg));
flag:
default:		0
DI_CHECK_ALIAS	0x10
DI_CHECK_INTERNAL_PATHS 0x20
DI_CHECK_MASK	0xf0

minor_nodetype:
DDI_NT_SERIAL			For serial ports
DDI_NT_SERAL_MB		For on board serial ports
DDI_NT_SERIAL_DO	For dial out ports
DDI_NT_SERAL_DO_MB	For on board dial out ports
DDI_NT_BLOCK			For hard disks
DDI_NT_BLOCK_CHAN	For hard disks with channel or target numbers
DDI_NT_CD				For CDROM drives
DDI_NT_CD_CHAN		For CDROM drives with channel or target numbers
DDI_NT_FD				For floppy disks
DDI_NT_TAPE				For tape drives
DDI_NT_NET				For DLPI style 1 or style 2 network devices
DDI_NT_DISPLAY		For display devices
DDI_PSEUDO				For pseudo devices
minor_callback:
DI_WALK_CONTINUE	Continue to visit subsequent minor data nodes
DI_WALK_TERMINATE	Terminate the walk immediately
Notice	: for network device, it is not accurate... use libdlpi.h -> dlpi_walk()
di_minor_t di_minor_next(di_node_t node,di_minor_t minor);

7
dev_t di_minor_devt(di_minor_t minor);
char * di_minor_name(di_minor_t minor);
char * di_minor_nodetype(di_minor_t minor);
int di_minor_spectype(di_minor_t minor);
return:		S_IFCHR or S_IFBLK

8
di_prop_t di_prop_next(di_node_t node,di_prop_t prop);

int di_prop_bytes(di_props_t prop,uchar_t  **prop_data);
dev_t di_prop_devt(di_props_t prop);
result:
DDI_DEV_T_NONE		the property is not associated with any specific minor node.
int di_prop_ints(di_props_t prop,int **prop_data);
int di_prop_int64(di_props_t prop,int64_t **prop_data);
char * di_prop_name(di_props_t prop);
int di_prop_strings(di_prop_t prop,char **prop_data);
int di_prop_type(di_props_t prop);
types:
DI_PROP_TYPE_BOOLEAN			always TRUE
DI_PROP_TYPE_INT						Use di_prop_ints()
DI_PROP_TYPE_INT64					Use di_prop_int64()
DI_PROP_TYPE_STRING				Use di_prop_strings()
DI_PROP_TYPE_BYTE					Use di_prop_bytes()
DI_PROP_TYPE_UNKNOWN			Use di_prop_bytes()
DI_PROP_TYPE_UNDEF_IT			No data available
DI_PROP_UNDEF_IT?
9
int di_prop_lookup_bytes(dev_t dev,di_node_t node,const char *prop_name,uchar_t **prop_data);
int di_prop_lookup_ints(dev_t dev,di_node_t node,const char *prop_name,int **prop_data);
int di_prop_lookup_int64(dev_t dev,di_node_t node,const char *prop_name,int64_t **prop_data);
int di_prop_lookup_strings(dev_t dev,di_node_t node,const char *prop_name,char **prop_data);

10
di_prom_handle_t di_prom_init(void);
void di_prom_fini(di_prom_handle_t ph);

di_prop_prop_t di_prom_prop_next(di_prom_handle_t ph, di_node_t node,di_prom_prop_t prom_prop);
char *di_prom_prop_name(di_prom_prop_t prom_prop)
int di_prom_prop_data(di_prom_prop_t prom_prop,uchar_t **prop_data);

/dev/openprom    :   read / change these prop

int di_prom_prop_lookup_bytes(di_prom_handle_t ph, di_node_t node,const char *prop_name,uchar_t **prop_data);
int di_prom_prop_lookup_ints(di_prom_handle_t ph, di_node_t node,const char *prop_name,int **prop_data);
int di_prom_prop_lookup_strings(di_prom_handle_t ph, di_node_t node,const char *prop_name,char **prop_data);

11 error in manual page
di_path_prop_t di_path_prop_next(di_path_t path,di_path_prop_t prop);
char *di_path_prop_name(di_path_prop_t prop);
int di_path_prop_type(di_path_prop_t prop);
int di_path_prop_len(di_path_prop_t prop); // does not exist in manual
int di_path_prop_bytes(di_path_prop_t prop,uchar_t **prop_data);
int di_path_prop_ints(di_path_prop_t prop,int **prop_data);
int di_path_prop_int64(di_path_prop_t prop,int64_t **prop_data);
int di_path_prop_strings(di_path_prop_t prop,char **prop_data);

12
int di_walk_link(di_node_t root,uint_t flag,uint_t endpoint, void*arg,int (*link_callback)(di_link_t link,void *arg));
endpoint:
DI_LINK_SRC
DI_LINK_TARGET
flag:		0
link_callback return value:
DI_WALK_CONTINUE
DI_WALK_TERMINATE

int di_walk_lnode(di_node_t root,uint_t flag,void* arg, int (*lnode_callback)(di_lnode_t link,void *arg));
flag:		0
lnode_callback return value:
DI_WALK_CONTINUE
DI_WALK_TERMINATE

//error in manual page
di_link_t di_link_next_by_node(di_node_t node,,di_link_t link, uint_t endpoint);
di_link_t di_link_next_by_lnode(di_lnode_t lnode,,di_link_t link, uint_t endpoint);
link:
handle of current link
DI_LINK_NIL
endpoint:
DI_LINK_TGT
DI_LINK_SRC

13
di_lnode_t di_lnode_next(di_node_t node,di_lnode_t lnode);
char * di_lnode_name(di_lnode_t lnode);
di_node_t di_lnode_devinfo(di_lnode_t lnode);
int di_lnode_devt(di_lnode_t,dev_t *devt);

int di_link_spectype(di_link_t link);
return:		S_IFCHR | S_IFBLK
di_lnode_t di_link_to_lnode(di_link_t link,uint_t endpoint);
*/
