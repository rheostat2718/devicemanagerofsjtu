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

static int node_init(nodeobj_t self,PyObject *args) {
	PyObject *root = NULL;
	if (!PyArg_ParseTuple(args,"|O",&root)) return -1;
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
	nodeobj_t n = (nodeobj_t) self;
	PyObject * dict = PyDict_New();
	PyDict_SetItem(dict, Py_BuildValue("s","name"),Py_BuildValue("s",di_node_name(n->node)));
	return dict;
}

static PyObject * node_child(PyObject * self,PyObject *args) {
	PyObject * list = PyList_New(0);
	return list;
}

static PyMethodDef node_methods[]={
		{"info",(PyCFunction)node_info,1,"Return node info"},
		{"child",(PyCFunction)node_child,1,"Return list of child nodes"},
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
