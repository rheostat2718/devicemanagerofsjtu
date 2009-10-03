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

static PyObject *DIError; /*local exception*/
#define onError(message) { PyErr_SetString(ErrorObject,message);return NULL;}

/*
 * Node type information
 */

typedef struct {
	PyObject_HEAD
	di_node_t node;
} nodeobject;

static struct PyMethodDef node_methods[] = {
//		{"info",node_info,1},
//		{"child",node_child,1},
		{NULL,NULL}
};

/*
 * Basic type operations
 */

static nodeobject * newnodeobject(PyObject *arg) {
	di_node_t root_node;
	nodeobject *tmp = malloc(sizeof(nodeobject));
	if (tmp == NULL) {
		PyErr_NoMemory();
		return NULL;
	}
//	if (!PyArg_Parse(arg,"")) return NULL;
	if ((root_node = di_init("/",DINFOCPYALL)) == DI_NODE_NIL) return NULL;
	tmp->node = root_node;
	return tmp;
}

static void node_dealloc(nodeobject *self) {
	di_fini(self->node);
	free(self);
}

static int node_print(nodeobject *self,FILE* fp,int flags) {

}

static PyObject * node_getattr(nodeobject *self,char* name) {

}

/*
 * Type descriptors
 */

static PyTypeObject Nodetype = {
		/* type header */
		PyObject_HEAD_INIT(NULL) /*PyObject_HEAD_INIT(&PyType_Type)*/
		0,/* ob_size */
		"stack",/* tp_name */
		sizeof(nodeobject),/* tp_basicsize */
		0,/* tp_itemsize */
		/* standard methods */
		(destructor) node_dealloc,/* tp_dealloc */
		(printfunc) node_print,/* tp_print */
		(getattrfunc) node_getattr,/* tp_getattr */
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
	printf("1");
	return (PyObject *)newnodeobject(args);
}

static struct PyMethodDef di_methods[] = {
		{"Node", nodetype_new,0,'Wrapped di_node_t class'},
		{NULL,NULL,0,NULL}
};

void initdi() {
	PyObject *m,*d;
	if (PyType_Ready(&Nodetype) < 0) return;
	m = Py_InitModule("di",di_methods);
	if (m == NULL) return;
	d = PyModule_GetDict(m);
	DIError = PyErr_NewException("di.error",NULL,NULL);
	Py_INCREF(DIError);
	PyModule_AddObject(m,"error",DIError);
}
