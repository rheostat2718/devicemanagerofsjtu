#ifndef DI_IMPL_H
#define DI_IMPL_H

#include <Python.h>
#include <structmember.h>
#include <libdevinfo.h>
#include <stdio.h>

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

typedef struct {
	PyObject_HEAD
	di_prop_t prop;
} propobj;

/* pointer types */
#define nodeobj_t nodeobj*
#define minorobj_t minorobj*
#define pathobj_t pathobj*
#define lnodeobj_t lnodeobj*
#define linkobj_t linkobj*
#define propobj_t propobj*
#define prompropobj_t prompropobj*

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
static PyObject * node_devid(PyObject * self,PyObject *args);
static PyObject * node_devfs_path(PyObject * self,PyObject *args);
static PyObject * node_driver_name(PyObject * self,PyObject *args);
static PyObject * node_driver_ops(PyObject * self,PyObject *args);
static PyObject * node_proplist(PyObject * self,PyObject *args);

static PyMethodDef node_methods[]={
		{"get_info",(PyCFunction)node_info,0,"Return node info"},
		{"get_child",(PyCFunction)node_child,1,"Return list of child nodes"},
		{"get_parent",(PyCFunction)node_parent,1,"Return parent node"},
		{"get_prop",(PyCFunction)node_proplist,1,"Return properties"},
		{"node_name",(PyCFunction)node_name,0,"Return node name"},
		{"bus_addr",(PyCFunction)node_bus_addr,0,"Return bus address"},
		{"binding_name",(PyCFunction)node_binding_name,0,"Return binding name"},
		{"compatible_names",(PyCFunction)node_compatible_names,0,"Return a list of compatible names"},
		{"instance",(PyCFunction)node_instance,0,"Return number of instance"},
		{"nodeid",(PyCFunction)node_nodeid,0,"Return nodeid"},
		{"driver_major",(PyCFunction)node_driver_major,0,"Return driver major number"},
		{"node_state",(PyCFunction)node_state,0,"Return node state"},
		{"state",(PyCFunction)node_distate,0,"Return state <not in Solaris manual>"},
		{"devid",(PyCFunction)node_devid,0,"Return node devid"},
		{"devfs_path",(PyCFunction)node_devfs_path,0,"Return device file path under /devices"},
		{"driver_name",(PyCFunction)node_driver_name,0,"Return driver name"},
		{"driver_ops",(PyCFunction)node_driver_ops,0,"Return driver options"},
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

static PyMethodDef prop_methods[]={
		{"get_name",(PyCFunction)prop_name,0,"Return property name"},
		{"get_type",(PyCFunction)prop_type,0,"Return property type id"},
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

#endif
