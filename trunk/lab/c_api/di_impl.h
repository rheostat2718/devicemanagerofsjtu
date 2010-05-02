#ifndef DI_IMPL_H
#define DI_IMPL_H

#include <Python.h>
#include <structmember.h>
#include <libdevinfo.h>
#include <stdio.h>
#include <strings.h>

#ifndef PyMODINIT_FUNC
#define PyMODINIT_FUNC void
#endif

/* Exception type*/
static PyObject *DIError; /* local exception */
#define onError(message) { PyErr_SetString(DIError,message);return NULL;}

/*
 * Type definitions
 */
typedef struct {
	PyObject_HEAD
	di_node_t node;
} nodeobj;

typedef struct {
	PyObject_HEAD
	di_minor_t minor;
} minorobj;

/*
typedef struct {
	PyObject_HEAD
	di_path_t path;
} pathobj;

typedef struct {
	PyObject_HEAD
	di_lnode_t lnode;
} lnodeobj;

typedef struct {
	PyObject_HEAD
	di_link_t link;
} linkobj;

typedef struct {
	PyObject_HEAD
	di_prom_prop_t promprop;
} prompropobj;
*/
typedef struct {
	PyObject_HEAD
	di_prop_t prop;
} propobj;

/* pointer types */
#define nodeobj_t nodeobj*
#define minorobj_t minorobj*
/*
#define pathobj_t pathobj*
#define lnodeobj_t lnodeobj*
#define linkobj_t linkobj*
#define prompropobj_t prompropobj*
*/
#define propobj_t propobj*

/* Node type operations */
static PyObject* node_new(PyTypeObject *type,PyObject *args,PyObject *kwds);
static int node_clear(nodeobj_t self);
static void node_dealloc(nodeobj_t self);
static int node_init(nodeobj_t self,PyObject *args,PyObject *kwds);

static PyMemberDef node_members[]={
		{"node",T_OBJECT_EX,offsetof(nodeobj,node),0,"node"},
		{NULL}/* Sentinel */
};

/* Node type methods */
static PyObject * node_info(PyObject * self,PyObject *args);
static PyObject * node_child(PyObject * self,PyObject *args);
static PyObject * node_parent(PyObject * self,PyObject *args);
static PyObject * node_name(PyObject * self,PyObject *args);
static PyObject * node_bus_addr(PyObject * self,PyObject *args);
static PyObject * node_binding_name(PyObject * self,PyObject *args);
static PyObject * node_compatible_names(PyObject * self,PyObject *args);
static PyObject * node_instance(PyObject * self,PyObject *args);
static PyObject * node_nodeid(PyObject * self,PyObject *args);
static PyObject * node_driver_major(PyObject * self,PyObject *args);
static PyObject * node_state(PyObject * self,PyObject *args);
static PyObject * node_distate(PyObject * self,PyObject *args);
//static PyObject * node_devid(PyObject * self,PyObject *args);
static PyObject * node_devfs_path(PyObject * self,PyObject *args);
static PyObject * node_driver_name(PyObject * self,PyObject *args);
static PyObject * node_driver_ops(PyObject * self,PyObject *args);
static PyObject * node_proplist(PyObject * self,PyObject *args);
static PyObject * node_minorlist(PyObject * self,PyObject *args);

static PyMethodDef node_methods[]={
		{"get_info",(PyCFunction)node_info,0,"Return node info"},
		{"get_children",(PyCFunction)node_child,1,"Return a list of children nodes"},
		{"get_parent",(PyCFunction)node_parent,1,"Return parent node"},
		{"get_prop",(PyCFunction)node_proplist,1,"Return node properties"},
		{"get_minor",(PyCFunction)node_minorlist,1,"Return minor nodes"},
		{"get_bus_addr",(PyCFunction)node_bus_addr,0,"Return bus address (di_bus_addr)"},
		{"get_binding_name",(PyCFunction)node_binding_name,0,"Return binding name (di_binding_name)"},
		{"get_compatible_name_list",(PyCFunction)node_compatible_names,0,"Return a list of compatible names (di_compatible_names)"},
		// (obsolete) di_devid, ignored
		{"get_driver_name",(PyCFunction)node_driver_name,0,"Return driver name, None for no driver (di_driver_name)"},
		{"get_driver_ops",(PyCFunction)node_driver_ops,0,"Return driver options (di_driver_ops)"},
		{"get_driver_major",(PyCFunction)node_driver_major,0,"Return driver major number, None for no driver (di_driver_major)"},
		{"get_instance_num",(PyCFunction)node_instance,0,"Return instance number, -1 for not assigned (di_instance)"},
		{"get_nodeid",(PyCFunction)node_nodeid,0,"Return type of device (di_nodeid)"},
		{"get_node_name",(PyCFunction)node_name,0,"Return node name (di_node_name)"},

		// value in header file, but not in manual
		{"node_state",(PyCFunction)node_state,0,"Return node state <not in Solaris manual>"},
		{"state",(PyCFunction)node_distate,0,"Return state <not in Solaris manual>"},

		{"devfs_path",(PyCFunction)node_devfs_path,0,"Return device file path under /devices"},
		{NULL} /*Sentinel*/
};

/* Node type descriptors */
static PyTypeObject NodeType = {/* type header */
		PyObject_HEAD_INIT(NULL) /*PyObject_HEAD_INIT(&PyType_Type)*/
		0,/* ob_size */
		"di.Node",/* tp_name */
		sizeof(nodeobj),/* tp_basicsize */
		0,/* tp_itemsize */

		/* standard methods */
		(destructor)node_dealloc,/* tp_dealloc */
		0,/* tp_print */
		0,/* tp_getattr */
		0,/* tp_setattr */
		0,/*tp_compare*/
		0,/*tp_repr*/

		/* type categories*/
		0,/*tp_as_number*/
		0,/*tp_as_sequence*/
		0,/*tp_as_mapping*/

		/* more methods */
		0,/*tp_hash*/
		0,/*tp_call*/
		0,/*tp_str*/
		0,/*tp_getattro*/
		0,/*tp_setattro*/
		0,/*tp_as_buffer*/

		Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,/*tp_flags*/
		"di_node objects",/*tp_doc*/
		0,/*tp_traverse*/
		(inquiry)node_clear,/*tp_clear*/
		0,/*tp_richcompare*/
		0,/*tp_weaklistoffset*/
		0,/*tp_iter*/
		0,/*tp_iternext*/
		node_methods,/*tp_methods*/
		node_members,/*tp_members*/
		0,/*tp_getset*/
		0,/*tp_base*/
		0,/*tp_dict*/
		0,/*tp_descr_get*/
		0,/*tp_descr_set*/
		0,/*tp_dictoff*/
		(initproc) node_init,/*tp_init*/
		0,/*tp_alloc*/
		node_new,/*tp_new*/
};

/* Prop type operations */
static PyObject* prop_new(PyTypeObject *type,PyObject *args,PyObject *kwds);
static int prop_clear(propobj_t self);
static void prop_dealloc(propobj_t self);
static int prop_init(propobj_t self,PyObject *args,PyObject *kwds);

static PyMemberDef prop_members[]={
		{"prop",T_OBJECT_EX,offsetof(propobj,prop),0,"prop"},
		{NULL}/* Sentinel */
};

/* Prop type methods */
static PyObject * prop_name(PyObject *self,PyObject *args);
static PyObject * prop_type(PyObject *self,PyObject *args);
static PyObject * prop_type_str(PyObject *self,PyObject *args);
static PyObject * prop_value(PyObject *self,PyObject *args);

static PyMethodDef prop_methods[]={
		{"get_name",(PyCFunction)prop_name,0,"Return property name (di_prop_name)"},
		{"get_type",(PyCFunction)prop_type,0,"Return property type id (di_prop_type)"},
		{"get_type_name",(PyCFunction)prop_type_str,0,"Return property type name"},
		{"get_value",(PyCFunction)prop_value,0,"Return property value(di_prop_bytes, ints, int64, strings)"},
		{NULL} /*Sentinel*/
};

/* Prop type descriptors */
static PyTypeObject PropType = {/* type header */
		PyObject_HEAD_INIT(NULL) /*PyObject_HEAD_INIT(&PyType_Type)*/
		0,/* ob_size */
		"di.Prop",/* tp_name */
		sizeof(propobj),/* tp_basicsize */
		0,/* tp_itemsize */

		/* standard methods */
		(destructor)prop_dealloc,/* tp_dealloc */
		0,/* tp_print */
		0,/* tp_getattr */
		0,/* tp_setattr */
		0,/*tp_compare*/
		0,/*tp_repr*/

		/* type categories*/
		0,/*tp_as_number*/
		0,/*tp_as_sequence*/
		0,/*tp_as_mapping*/

		/* more methods */
		0,/*tp_hash*/
		0,/*tp_call*/
		0,/*tp_str*/
		0,/*tp_getattro*/
		0,/*tp_setattro*/
		0,/*tp_as_buffer*/

		Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,/*tp_flags*/
		"di_prop_t objects",/*tp_doc*/
		0,/*tp_traverse*/
		(inquiry)prop_clear,/*tp_clear*/
		0,/*tp_richcompare*/
		0,/*tp_weaklistoffset*/
		0,/*tp_iter*/
		0,/*tp_iternext*/
		prop_methods,/*tp_methods*/
		prop_members,/*tp_members*/
		0,/*tp_getset*/
		0,/*tp_base*/
		0,/*tp_dict*/
		0,/*tp_descr_get*/
		0,/*tp_descr_set*/
		0,/*tp_dictoff*/
		(initproc) prop_init,/*tp_init*/
		0,/*tp_alloc*/
		prop_new,/*tp_new*/
};

/* Minor type operations */
static PyObject* minor_new(PyTypeObject *type,PyObject *args,PyObject *kwds);
static int minor_clear(minorobj_t self);
static void minor_dealloc(minorobj_t self);
static int minor_init(minorobj_t self,PyObject *args,PyObject *kwds);

static PyMemberDef minor_members[]={
		{"minor",T_OBJECT_EX,offsetof(minorobj,minor),0,"minor"},
		{NULL}/* Sentinel */
};

/* Minor type methods */
static PyObject * minor_devfs_path(PyObject * self,PyObject *args);
static PyObject * minor_name(PyObject * self,PyObject *args);
static PyObject * minor_nodetype(PyObject * self,PyObject *args);
static PyObject * minor_spectype(PyObject * self,PyObject *args);
static PyObject * minor_info(PyObject * self,PyObject *args);

static PyMethodDef minor_methods[]={
		{"get_name",(PyCFunction)minor_name,0,"Return minor node name (di_minor_name)"},
		{"get_nodetype",(PyCFunction)minor_nodetype,0,"Return minor node nodetype (di_minor_nodetype)"},
		{"get_spectype",(PyCFunction)minor_spectype,0,"Return minor node spectype (di_minor_spectype)"},
		{"get_devfs_path",(PyCFunction)minor_devfs_path,0,"Return minor node devfs path (di_devfs_minor_path)"},
		{"get_info",(PyCFunction)minor_info,0,"Return minor node info"},
		{NULL} /*Sentinel*/
};

/* Minor type descriptors */
static PyTypeObject MinorType = {/* type header */
		PyObject_HEAD_INIT(NULL) /*PyObject_HEAD_INIT(&PyType_Type)*/
		0,/* ob_size */
		"di.Minor",/* tp_name */
		sizeof(minorobj),/* tp_basicsize */
		0,/* tp_itemsize */

		/* standard methods */
		(destructor)minor_dealloc,/* tp_dealloc */
		0,/* tp_print */
		0,/* tp_getattr */
		0,/* tp_setattr */
		0,/*tp_compare*/
		0,/*tp_repr*/

		/* type categories*/
		0,/*tp_as_number*/
		0,/*tp_as_sequence*/
		0,/*tp_as_mapping*/

		/* more methods */
		0,/*tp_hash*/
		0,/*tp_call*/
		0,/*tp_str*/
		0,/*tp_getattro*/
		0,/*tp_setattro*/
		0,/*tp_as_buffer*/

		Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,/*tp_flags*/
		"di_minor_t objects",/*tp_doc*/
		0,/*tp_traverse*/
		(inquiry)minor_clear,/*tp_clear*/
		0,/*tp_richcompare*/
		0,/*tp_weaklistoffset*/
		0,/*tp_iter*/
		0,/*tp_iternext*/
		minor_methods,/*tp_methods*/
		minor_members,/*tp_members*/
		0,/*tp_getset*/
		0,/*tp_base*/
		0,/*tp_dict*/
		0,/*tp_descr_get*/
		0,/*tp_descr_set*/
		0,/*tp_dictoff*/
		(initproc) minor_init,/*tp_init*/
		0,/*tp_alloc*/
		minor_new,/*tp_new*/
};

#endif
