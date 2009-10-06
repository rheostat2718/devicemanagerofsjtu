/*
 * di.c: wrap C library devinfo into Python code
 * This file intends to return Python objects such as:
 * di_node_t node
 * di_minor_t minor
 * di_path_t path
 * di_lnode_t lnode
 * di_link_t link
 */

#include <Python.h>
#include <structmember.h>
#include <libdevinfo.h>
#include <stdio.h>

static PyObject *DIError; /* local exception */
#define onError(message) { PyErr_SetString(DIError,message);return NULL;}

/*
 * Node type information
 */
typedef struct {
	PyObject_HEAD
	di_node_t node;
} nodeobj;

#define nodeobj_t nodeobj*

/*
 * Basic type operations
 */

static PyObject* node_new(PyTypeObject *type,PyObject *args,PyObject *kwds) {
	nodeobj_t self;
	self = (nodeobj_t) type->tp_alloc(type,0);
	if (self == NULL) {
		PyErr_NoMemory();
		return NULL;
	}
	if ((self->node = di_init("/",DINFOCPYALL)) == DI_NODE_NIL) {
		Py_DECREF(self);
		return NULL;
		/*onError("Cannot init root node")*/
	}
	return (PyObject *)self;
}

static void node_dealloc(nodeobj_t self) {
	di_node_t tmp = NULL;
	if (self != NULL) {
		if (self->node != NULL) di_fini(self->node);
		self->ob_type->tp_free((PyObject*)self);
	}
}

static int node_init(nodeobj_t self,PyObject *args,PyObject *kwds) {
	PyObject *root = NULL;
	static char *kwlist[] {"node",NULL};
	if (!PyArg_ParseTupleAndKeywords(args,kwds,"|O",kwlist,&root)) return -1;
	if (root) {
		self->node = ((nodeobj_t)root)->node;
	}
	else {
		if ((self->node = di_init("/",DINFOCPYALL))==DI_NODE_NIL) {
			Py_XDECREF(self);
			return -1;
		}
	}
	return 0;
}

static PyMemberDef node_members[]={
		{"node",T_OBJECT_EX,offsetof(nodeobj,node),0,"node"},
		{NULL}/* Sentinel */
};

static PyObject * node_info(PyObject * self,PyObject *args) {
	di_node_t node = (nodeobj_t) self->node;
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
	PyDict_SetItem(dict, Py_BuildValue("s","compatible_names_count"),Py_BuildValue("i",count));
	while (count > 0) {
		PyList_Append(compat,Py_BuildValue("s",name));
		name = name+strlen(name)+1;
		count -= 1;
	}
	PyDict_SetItem(dict, Py_BuildValue("s","compatible_names"),compat);
	PyDict_SetItem(dict,Py_BuildValue("s","instance"),Py_BuildValue("i",di_instance(node)));
	PyDict_SetItem(dict,Py_BuildValue("s","id"),Py_BuildValue("i",id));
	if (id & DI_PSEUDO_NODEID)
		PyDict_SetItem(dict,Py_BuildValue("s","id_pseudo"),Py_BuildValue("s","True"));
	else
		PyDict_SetItem(dict,Py_BuildValue("s","id_pseudo"),Py_BuildValue("s","False"));
	if (id & DI_PROM_NODEID)
		PyDict_SetItem(dict,Py_BuildValue("s","id_prom"),Py_BuildValue("s","True"));
		//have additional properties : di_prom_prop_data di_prom_prop_lookup_bytes
	else
		PyDict_SetItem(dict,Py_BuildValue("s","id_prom"),Py_BuildValue("s","False"));
	if (id & DI_SID_NODEID)
		PyDict_SetItem(dict,Py_BuildValue("s","id_sid"),Py_BuildValue("s","True"));
	else
		PyDict_SetItem(dict,Py_BuildValue("s","id_sid"),Py_BuildValue("s","False"));
	PyDict_SetItem(dict,Py_BuildValue("s","driver_major"),Py_BuildValue("i",di_driver_major(node)));
	PyDict_SetItem(dict,Py_BuildValue("s","state"),Py_BuildValue("l",di_state(node)));
	PyDict_SetItem(dict,Py_BuildValue("s","node_state"),Py_BuildValue("l",state));
	if (state & DI_DRIVER_DETACHED)
		PyDict_SetItem(dict,Py_BuildValue("s","node_state_driver_detached"),Py_BuildValue("s","True"));
	else
		PyDict_SetItem(dict,Py_BuildValue("s","node_state_driver_detached"),Py_BuildValue("s","False"));
	if (state & DI_DEVICE_OFFLINE)
		PyDict_SetItem(dict,Py_BuildValue("s","node_state_device_offline"),Py_BuildValue("s","True"));
	else
		PyDict_SetItem(dict,Py_BuildValue("s","node_state_device_offline"),Py_BuildValue("s","False"));
	if (state & DI_DEVICE_DOWN)
		PyDict_SetItem(dict,Py_BuildValue("s","node_state_device_down"),Py_BuildValue("s","True"));
	else
		PyDict_SetItem(dict,Py_BuildValue("s","node_state_device_down"),Py_BuildValue("s","False"));
	if (state & DI_DEVICE_DEGRADED)
		PyDict_SetItem(dict,Py_BuildValue("s","node_state_device_degraded"),Py_BuildValue("s","True"));
	else
		PyDict_SetItem(dict,Py_BuildValue("s","node_state_device_degraded"),Py_BuildValue("s","False"));
	if (state & DI_BUS_QUIESCED)
		PyDict_SetItem(dict,Py_BuildValue("s","node_state_bus_quiesced"),Py_BuildValue("s","True"));
	else
		PyDict_SetItem(dict,Py_BuildValue("s","node_state_bus_quiesced"),Py_BuildValue("s","False"));
	if (state & DI_BUS_DOWN)
		PyDict_SetItem(dict,Py_BuildValue("s","node_state_bus_down"),Py_BuildValue("s","True"));
	else
		PyDict_SetItem(dict,Py_BuildValue("s","node_state_bus_down"),Py_BuildValue("s","False"));
	PyDict_SetItem(dict,Py_BuildValue("s","devid"),Py_BuildValue("l",di_devid(node)));
	PyDict_SetItem(dict,Py_BuildValue("s","driver_name"),Py_BuildValue("s",di_driver_name(node)));
	PyDict_SetItem(dict,Py_BuildValue("s","driver_ops"),Py_BuildValue("l",ops));
	if (ops & DI_CB_OPS)
		PyDict_SetItem(dict,Py_BuildValue("s","driver_cb_ops"),Py_BuildValue("s","True"));
	else
		PyDict_SetItem(dict,Py_BuildValue("s","driver_cb_ops"),Py_BuildValue("s","False"));
	if (ops & DI_BUS_OPS)
		PyDict_SetItem(dict,Py_BuildValue("s","driver_bus_ops"),Py_BuildValue("s","True"));
	else
		PyDict_SetItem(dict,Py_BuildValue("s","driver_bus_ops"),Py_BuildValue("s","False"));
	if (ops & DI_STREAM_OPS)
		PyDict_SetItem(dict,Py_BuildValue("s","driver_stream_ops"),Py_BuildValue("s","True"));
	else
		PyDict_SetItem(dict,Py_BuildValue("s","driver_stream_ops"),Py_BuildValue("s","False"));

	PyDict_SetItem(dict,Py_BuildValue("s","devfs_path"),Py_BuildValue("s",(di_devfs_path(node))));
	return dict;
}

static PyObject * node_child(PyObject * self,PyObject *args) {
	PyObject * list = PyList_New(0);
	return list;
}

static PyObject * node_minor(PyObject *self,PyObject *args) {
	return Py_None();
}

static PyMethodDef node_methods[]={
		{"get_info",(PyCFunction)node_info,1,"Return node info"},
		{"get_child",(PyCFunction)node_child,1,"Return list of child nodes"},
		{NULL} /*Sentinel*/
};

/*
 * Type descriptors
 */

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
		0,/*tp_clear*/
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
		(initproc) node_init,/*tp_init*/ //node_init
		0,/*tp_alloc*/
		node_new,/*tp_new*/
};

/* module logic */
static struct PyMethodDef di_methods[] = {
		{NULL}
};

#ifndef PyMODINIT_FUNC
#define PyMODINIT_FUNC void
#endif

PyMODINIT_FUNC initdi(void) {
	PyObject *m,*d;
	if (PyType_Ready(&NodeType) < 0) return;
	m = Py_InitModule3("di",di_methods,"libdevinfo in Python");
	if (m == NULL) return;
	Py_INCREF(&NodeType);
	PyModule_AddObject(m,"Node",(PyObject*)&NodeType);

	d = PyModule_GetDict(m);
	DIError = PyErr_NewException("di.error",NULL,NULL);
	Py_INCREF(DIError);
	PyModule_AddObject(m,"error",DIError);
}

/*
static PyGetSetDef node_getseters[]={
	{"flag",(getter)node_getflag,(setter)node_setflag,"flag"},
	{NULL}
};
 */
