/*
 * di.c: a wrap of C library devinfo into Python code
 * This file intends to return Python objects such as:
 * di_node_t node
 * di_minor_t minor
 * di_path_t path
 * di_lnode_t lnode
 * di_link_t link
 */

#include <Python.h>
#include <libdevinfo.h>

static PyObject *DIError; /* local exception */
#define onError(message) { PyErr_SetString(DIError,message);return NULL;}

/*
 * Node type information
 */
typedef struct {
	PyObject_HEAD
	di_node_t node;
} nodeobject;

#define nodeobj_t nodeobject*

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

static struct PyMethodDef node_methods[] = {
	{"info",node_info,1},
	{"child",node_child,1},
	{NULL,NULL,0}
};

/*
 * Basic type operations
 */

static nodeobject * newnodeobject(nodeobject *arg) {
	nodeobj_t tmp = malloc(sizeof(nodeobject));
	if (tmp == NULL) {
		PyErr_NoMemory();
		return NULL;
	}
	if ((tmp->node = di_init("/",DINFOCPYALL)) == DI_NODE_NIL) onError("Cannot init root node");
	return tmp;
}

static void node_dealloc(nodeobject *self) {
	printf("dealloc");
	if (self != NULL) {
		if (self->node != NULL) {
			di_fini(self->node);
		}
		printf("free\n");
		free(self);
	}
}

/*
 * Type descriptors
 */

static PyTypeObject NodeType = {
		/* type header */
		PyObject_HEAD_INIT(NULL) /*PyObject_HEAD_INIT(&PyType_Type)*/
		0,/* ob_size */
		"Node",/* tp_name */
		sizeof(nodeobject),/* tp_basicsize */
		0,/* tp_itemsize */
		/* standard methods */
		(destructor) node_dealloc,/* tp_dealloc */
		(printfunc) 0,/* tp_print */
		(getattrfunc) 0,/* tp_getattr */
		(setattrfunc) 0,/* tp_setattr */
		(cmpfunc) 0,/*tp_compare*/
		(reprfunc) 0,/*tp_repr*/
		/* type categories*/
		0,/*tp_as_number*/
		0,/*tp_as_sequence*/
		0,/*tp_as_mapping*/
		/* more methods */
		(hashfunc) 0,/*tp_hash*/
		(ternaryfunc) 0,/*tp_call*/
		(reprfunc) 0,/*tp_str*/
};

/* module logic */
static PyObject * nodetype_new(PyObject *self,PyObject *args) {
	if (!PyArg_ParseTuple(args,"")) return NULL;
	return (PyObject *)newnodeobject(NULL);
}

static struct PyMethodDef di_methods[] = {
		{"Node", nodetype_new,1,"Wrapped di_node_t class"},
		{NULL,NULL,0,NULL}
};

PyMODINIT_FUNC initdi(void) {
	PyObject *m,*d;
	if (PyType_Ready(&NodeType) < 0) return;
	m = Py_InitModule("di",di_methods);
	if (m == NULL) return;
	d = PyModule_GetDict(m);
	DIError = PyErr_NewException("di.error",NULL,NULL);
	Py_INCREF(DIError);
	PyModule_AddObject(m,"error",DIError);
}
