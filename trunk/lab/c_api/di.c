/*
 * di.c: wrap C library devinfo into Python code
 * This program intends to return Python version types ->
 * di_node_t node
 * di_minor_t minor
 * di_path_t path
 * di_lnode_t lnode
 * di_link_t link
 * ???????_t prop
 */

#include "di.h"

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
		onError("Cannot init root node")
	}
	return (PyObject *)self;
}

static int node_clear(nodeobj_t self) {
	if (self != NULL)
		if (self -> node != NULL)
			di_fini(self -> node);
	return 0;
}

static void node_dealloc(nodeobj_t self) {
	node_clear(self);
	self->ob_type->tp_free((PyObject*)self);
}

static int node_init(nodeobj_t self,PyObject *args,PyObject *kwds) {
	PyObject *root = NULL;
	static char *kwlist[]={"node",NULL};
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

static PyObject * node_name(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("s",di_node_name(node));
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_bus_addr(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("s",di_bus_addr(node));
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_binding_name(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("s",di_binding_name(node));
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_compatible_names(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL) {
		PyObject * compat = PyList_New(0);
		char * name = NULL;
		int count = di_compatible_names(node,&name);
		while (count > 0) {
			PyList_Append(compat,Py_BuildValue("s",name));
			name = name+strlen(name)+1;
			count -= 1;
		}
		return compat;
	}
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_instance(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("l",di_instance(node));
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_nodeid(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("l",di_nodeid(node));
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_driver_major(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("l",di_driver_major(node));
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_state(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("l",di_node_state(node));
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_distate(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("l",di_state(node));
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_devid(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("l",di_devid(node));
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_devfs_path(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("s",di_devfs_path(node));
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_driver_ops(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("l",di_driver_ops(node));
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_driver_name(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("s",di_driver_name(node));
	else
		onError("cannot access node : DI_NODE_NIL")
}

static PyObject * node_info(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t)self)->node;
	PyObject * dict = PyDict_New();
	int id = di_nodeid(node);
	int state = di_node_state(node);
	int ops = di_driver_ops(node);
	if (!PyArg_Parse(args,"")) return NULL;
	PyDict_SetItem(dict, Py_BuildValue("s","name"),node_name(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","addr"),node_bus_addr(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","binding_name"),node_binding_name(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","compatible_names"),node_compatible_names(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","instance"),node_instance(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","nodeid"),node_nodeid(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","state"),node_distate(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","node_state"),node_state(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","devid"),node_devid(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","devfs_path"),node_devfs_path(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","driver_name"),node_driver_name(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","driver_ops"),node_driver_ops(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","driver_major"),node_driver_major(self,args));

/*	if (id & DI_PSEUDO_NODEID)
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
	*/
	return dict;
}

static PyObject * node_child(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t)self)->node;
	PyObject * list = PyList_New(0);
	di_node_t child_node = di_child_node(node);

	if (!PyArg_Parse(args,"()")) return NULL;

	while (child_node != DI_NODE_NIL) {
		nodeobj_t child = self->ob_type->tp_new(self->ob_type,Py_BuildValue(""),Py_BuildValue(""));
		child->node = child_node;
		PyList_Append(list,(PyObject *)child);
		child_node = di_sibling_node(child_node);
	}
	return list;
}

/*static PyObject * node_minor(PyObject *self,PyObject *args) {
	return PyNone();
}*/

static PyObject * node_parent(PyObject * self,PyObject *args) {
/*	if (!PyObject_TypeCheck(self,&nodeobj)) {
		PyErr_SetString(PyExc_TypeError,"self is not a Node");
		return NULL;
	}*/
	di_node_t node = ((nodeobj_t)self)->node;
	di_node_t parent_node = di_parent_node(node);
	nodeobj_t parent = self->ob_type->tp_new(self->ob_type,Py_BuildValue(""),Py_BuildValue(""));

	if (!PyArg_Parse(args,"()")) return NULL;

	parent->node = parent_node;
	return (PyObject *) parent;
}

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
