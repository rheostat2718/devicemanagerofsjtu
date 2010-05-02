/*
 * di.c di.h : wrap C library devinfo into Python code
 * The program intends to return PyObject :
 * di_node_t 		node		=========-
 * di_minor_t 		minor		----------
 * di_path_t 		path		----------
 * di_lnode_t 		lnode		----------
 * di_link_t 		link		----------
 * di_prop_t 		prop		=======---
 * di_prom_prop_t 	promprop	----------
 */

#include "di_impl.h"

/* di Module logic */
static struct PyMethodDef di_methods[] = {
		{NULL}
};

static void add_const(PyObject *mod) {
	DIError = PyErr_NewException("di.error",NULL,NULL);
	Py_INCREF(DIError);
	PyModule_AddObject(mod,"error",DIError);
/* di_walk_node, not used*/
	PyModule_AddObject(mod,"DI_WALK_CLDFIRST",Py_BuildValue("i",DI_WALK_CLDFIRST));
	PyModule_AddObject(mod,"DI_WALK_SIBFIRST",Py_BuildValue("i",DI_WALK_SIBFIRST));
	PyModule_AddObject(mod,"DI_WALK_LINKGEN",Py_BuildValue("i",DI_WALK_LINKGEN));
	PyModule_AddObject(mod,"DI_WALK_MASK",Py_BuildValue("i",DI_WALK_MASK));
/* di_walk_node callback, not used currently*/
	PyModule_AddObject(mod,"DI_WALK_CONTINUE",Py_BuildValue("i",DI_WALK_CONTINUE)); //Continue walking
	PyModule_AddObject(mod,"DI_WALK_PRUNESIB",Py_BuildValue("i",DI_WALK_PRUNESIB)); //Continue walking, but skip siblings and their child nodes
	PyModule_AddObject(mod,"DI_WALK_PRUNECHILD",Py_BuildValue("i",DI_WALK_PRUNECHILD)); //Continue walking,but skip subtree rooted at current node
	PyModule_AddObject(mod,"DI_WALK_TERMINATE",Py_BuildValue("i",DI_WALK_TERMINATE)); //Terminate the walk immediately.
/* di_node_xx, export to Python*/
	PyModule_AddObject(mod,"DI_PSEUDO_NODEID",Py_BuildValue("i",DI_PSEUDO_NODEID));
	PyModule_AddObject(mod,"DI_PROM_NODEID",Py_BuildValue("i",DI_PROM_NODEID));
	PyModule_AddObject(mod,"DI_SID_NODEID",Py_BuildValue("i",DI_SID_NODEID));
	PyModule_AddObject(mod,"DI_DRIVER_DETACHED",Py_BuildValue("i",DI_DRIVER_DETACHED));
	PyModule_AddObject(mod,"DI_DEVICE_OFFLINE",Py_BuildValue("i",DI_DEVICE_OFFLINE));
	PyModule_AddObject(mod,"DI_DEVICE_DOWN",Py_BuildValue("i",DI_DEVICE_DOWN));
	PyModule_AddObject(mod,"DI_DEVICE_DEGRADED",Py_BuildValue("i",DI_DEVICE_DEGRADED));
	PyModule_AddObject(mod,"DI_BUS_QUIESCED",Py_BuildValue("i",DI_BUS_QUIESCED));
	PyModule_AddObject(mod,"DI_BUS_DOWN",Py_BuildValue("i",DI_BUS_DOWN));
	PyModule_AddObject(mod,"DI_PROP_TYPE_BOOLEAN",Py_BuildValue("i",DI_PROP_TYPE_BOOLEAN));
	PyModule_AddObject(mod,"DI_PROP_TYPE_INT",Py_BuildValue("i",DI_PROP_TYPE_INT));
	PyModule_AddObject(mod,"DI_PROP_TYPE_INT64",Py_BuildValue("i",DI_PROP_TYPE_INT64));
	PyModule_AddObject(mod,"DI_PROP_TYPE_STRING",Py_BuildValue("i",DI_PROP_TYPE_STRING));
	PyModule_AddObject(mod,"DI_PROP_TYPE_BYTE",Py_BuildValue("i",DI_PROP_TYPE_BYTE));
	PyModule_AddObject(mod,"DI_PROP_TYPE_UNKNOWN",Py_BuildValue("i",DI_PROP_TYPE_UNKNOWN));
	PyModule_AddObject(mod,"DI_PROP_TYPE_UNDEF_IT",Py_BuildValue("i",DI_PROP_TYPE_UNDEF_IT));
}

PyMODINIT_FUNC initdi(void) {
	PyObject *m;
	if (PyType_Ready(&NodeType) < 0) return;
	if (PyType_Ready(&PropType) < 0) return;
	if (PyType_Ready(&MinorType) < 0) return;
	m = Py_InitModule3("di",di_methods,"ports of libdevinfo in Python");
	if (m == NULL) return;

	Py_INCREF(&NodeType);
	Py_INCREF(&PropType);
	Py_INCREF(&MinorType);
	PyModule_AddObject(m,"Node",(PyObject*)&NodeType);
	PyModule_AddObject(m,"Prop",(PyObject*)&PropType);
	PyModule_AddObject(m,"Minor",(PyObject*)&MinorType);
	add_const(m);
}

/*
 * node - Basic type operations
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
		onError("Cannot initialize root node");
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

/*
 * node - Methods
 */
static PyObject * node_name(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("s",di_node_name(node));
	else
		onError("cannot access node : DI_NODE_NIL");
}

static PyObject * node_bus_addr(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("s",di_bus_addr(node));
	else
		onError("cannot access node : DI_NODE_NIL");
}

static PyObject * node_binding_name(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("s",di_binding_name(node));
	else
		onError("cannot access node : DI_NODE_NIL");
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
		onError("cannot access node : DI_NODE_NIL");
}

static PyObject * node_instance(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("l",di_instance(node));
	else
		onError("cannot access node : DI_NODE_NIL");
}

static PyObject * node_nodeid(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("l",di_nodeid(node));
	else
		onError("cannot access node : DI_NODE_NIL");
}

static PyObject * node_driver_major(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL) {
		long ret = di_driver_major(node);
		if (ret != -1)
			return Py_BuildValue("l",ret);
		else
			Py_RETURN_NONE;
	}
	else
		onError("cannot access node : DI_NODE_NIL");
}

static PyObject * node_state(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("l",di_node_state(node));
	else
		onError("cannot access node : DI_NODE_NIL");
}

static PyObject * node_distate(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("l",di_state(node));
	else
		onError("cannot access node : DI_NODE_NIL");
}

static PyObject * node_devfs_path(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL) {
		char *dpath = di_devfs_path(node);
		PyObject *ret = Py_BuildValue("s",dpath);
		di_devfs_path_free(dpath);
		return ret;
	}
	else
		onError("cannot access node : DI_NODE_NIL");
}

static PyObject * node_driver_ops(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("l",di_driver_ops(node));
	else
		onError("cannot access node : DI_NODE_NIL");
}

static PyObject * node_driver_name(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t) self)->node;
	if (!PyArg_Parse(args,"")) return NULL;
	if (node != DI_NODE_NIL)
		return Py_BuildValue("s",di_driver_name(node));
	else
		onError("cannot access node : DI_NODE_NIL");
}

static PyObject * node_info(PyObject * self,PyObject *args) {
	di_node_t node = ((nodeobj_t)self)->node;
	PyObject * dict = PyDict_New();
	int id = di_nodeid(node);
	int state = di_node_state(node);
	int ops = di_driver_ops(node);
	if (!PyArg_Parse(args,"")) return NULL;
	PyDict_SetItem(dict, Py_BuildValue("s","node name"),node_name(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","bus address"),node_bus_addr(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","binding name"),node_binding_name(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","compatible name"),node_compatible_names(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","instance"),node_instance(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","nodeid"),node_nodeid(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","state"),node_distate(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","node state"),node_state(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","devfs path"),node_devfs_path(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","driver name"),node_driver_name(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","driver ops"),node_driver_ops(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","driver major"),node_driver_major(self,args));

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
		nodeobj_t child = (nodeobj_t)self->ob_type->tp_new(self->ob_type,Py_BuildValue(""),Py_BuildValue(""));
		child->node = child_node;
		PyList_Append(list,(PyObject *)child);
		child_node = di_sibling_node(child_node);
	}
	return list;
}

static PyObject * node_minorlist(PyObject *self,PyObject *args) {
	di_node_t node = ((nodeobj_t)self)->node;
	PyObject * list = PyList_New(0);
	di_minor_t minor_next = di_minor_next(node,DI_MINOR_NIL);
	while (minor_next != DI_MINOR_NIL) {
		minorobj_t minor = (minorobj_t) minor_new(&MinorType,Py_BuildValue(""),Py_BuildValue(""));
		minor->minor = minor_next;
		PyList_Append(list,(PyObject *)minor);
		minor_next = di_minor_next(node,minor_next);
	}
	return list;
}

static PyObject * node_proplist(PyObject *self,PyObject *args) {
	di_node_t node = ((nodeobj_t)self)->node;
	PyObject * list = PyList_New(0);
	di_prop_t prop_next = di_prop_next(node,DI_PROP_NIL);
	while (prop_next != DI_PROP_NIL) {
		propobj_t prop = (propobj_t) prop_new(&PropType,Py_BuildValue(""),Py_BuildValue(""));
		prop->prop = prop_next;
		PyList_Append(list,(PyObject *)prop);
		prop_next = di_prop_next(node,prop_next);
	}
	return list;
}

static PyObject * node_parent(PyObject * self,PyObject *args) {
/*	if (!PyObject_TypeCheck(self,&nodeobj)) {
		PyErr_SetString(PyExc_TypeError,"self is not a Node");
		return NULL;
	}*/
	di_node_t node = ((nodeobj_t)self)->node;
	di_node_t parent_node = di_parent_node(node);
	nodeobj_t parent = (nodeobj_t) self->ob_type->tp_new(self->ob_type,Py_BuildValue(""),Py_BuildValue(""));

	if (!PyArg_Parse(args,"()")) return NULL;

	parent->node = parent_node;
	return (PyObject *) parent;
}

/*
 * prop - Basic type operations
 */

static PyObject* prop_new(PyTypeObject *type,PyObject *args,PyObject *kwds) {
	propobj_t self = (propobj_t) type->tp_alloc(type,0);
	if (self == NULL) {
		PyErr_NoMemory();
		return NULL;
	}
	self->prop = NULL;
	return (PyObject *)self;
}

static int prop_clear(propobj_t self) {
	if (self != NULL)
		if (self -> prop != NULL)
			self -> prop = NULL;
	return 0;
}

static void prop_dealloc(propobj_t self) {
	prop_clear(self);
	self->ob_type->tp_free((PyObject*)self);
}

static int prop_init(propobj_t self,PyObject *args,PyObject *kwds) {
	PyObject *root = NULL;
	static char *kwlist[]={"prop",NULL};
	if (!PyArg_ParseTupleAndKeywords(args,kwds,"|O",kwlist,&root)) return -1;
	if (root) {
		self->prop = ((propobj_t)root)->prop;
	}
	else {
		self->prop = NULL;
	}
	return 0;
}

/*
 * prop - Methods
 */
static PyObject * prop_name(PyObject * self,PyObject *args) {
	di_prop_t prop = ((propobj_t) self)->prop;
	if (!PyArg_Parse(args,"")) return NULL;
	if (prop != DI_PROP_NIL)
		return Py_BuildValue("s",di_prop_name(prop));
	else
		onError("cannot access prop : DI_PROP_NIL");
}

static PyObject * prop_type(PyObject * self,PyObject * args) {
	di_prop_t prop = ((propobj_t) self)->prop;
	if (!PyArg_Parse(args,"")) return NULL;
	if (prop != DI_PROP_NIL)
		return Py_BuildValue("i",di_prop_type(prop));
	else
		onError("cannot access prop : DI_PROP_NIL");
}

static PyObject * prop_type_str(PyObject *self, PyObject *args) {
	di_prop_t prop = ((propobj_t) self)->prop;
	if (!PyArg_Parse(args,"")) return NULL;
	if (prop != DI_PROP_NIL)
		switch (di_prop_type(prop)) {
		case DI_PROP_TYPE_BOOLEAN:return Py_BuildValue("s","boolean");
		case DI_PROP_TYPE_UNDEF_IT:return Py_BuildValue("s","None");
		case DI_PROP_TYPE_INT:return Py_BuildValue("s","list of int");
		case DI_PROP_TYPE_INT64:return Py_BuildValue("s","list of 64-bit int");
		case DI_PROP_TYPE_STRING:return Py_BuildValue("s","list of strings");
		case DI_PROP_TYPE_BYTE:return Py_BuildValue("s","list of bytes");
		case DI_PROP_TYPE_UNKNOWN:return Py_BuildValue("s","unknown type");
		default:break;
		}
	onError("cannot access prop : DI_PROP_NIL");
}

static PyObject * prop_value(PyObject *self, PyObject *args) {
	di_prop_t prop = ((propobj_t) self)->prop;
	int i;
	PyObject *list = NULL;

	if (!PyArg_Parse(args,"")) return NULL;
	int type = di_prop_type(prop);
	switch (type) {
	case DI_PROP_TYPE_BOOLEAN:{
		Py_RETURN_TRUE;
	}
	case DI_PROP_TYPE_UNKNOWN:{
		uchar_t *values = NULL;
		int count = di_prop_bytes(prop,&values);

		if (values == NULL)
			onError("Cannot get property value");
		list = PyList_New(0);
		for (i=0;i<count;i++) {
			PyList_Append(list,Py_BuildValue("b",values[i]));
		}
		return list;
	}
	case DI_PROP_TYPE_UNDEF_IT:{
		Py_RETURN_NONE;
	}
	case DI_PROP_TYPE_BYTE:{
		uchar_t *values = NULL;
		int count = di_prop_bytes(prop,&values);

		if (values == NULL)
			onError("Cannot get property value");
		list = PyList_New(0);
		for (i=0;i<count;i++) {
			PyList_Append(list,Py_BuildValue("b",values[i]));
		}
		return list;
	}
	case DI_PROP_TYPE_INT:{
		int *values = NULL;
		int count = di_prop_ints(prop,&values);

		if (values == NULL)
			onError("Cannot get property value");

		list = PyList_New(0);
		for (i=0;i<count;i++) {
			PyList_Append(list,Py_BuildValue("i",values[i]));
		}
		return list;
	}
	case DI_PROP_TYPE_INT64:{
		int64_t *values = NULL;//PyLong_FromLongLong()
		int count = di_prop_int64(prop,&values);

		if (values == NULL)
			onError("Cannot get property value");

		list = PyList_New(0);
		for (i=0;i<count;i++) {
			PyList_Append(list,Py_BuildValue("K",values[i]));
		}
		return list;
	}
	case DI_PROP_TYPE_STRING:{
		char *values = NULL;
		int count = di_prop_strings(prop,&values);

		if (values == NULL)
			onError("Cannot get property value");

		list = PyList_New(0);
		char *start = values;
		for (i=0;i<count;i++) {
			PyList_Append(list,Py_BuildValue("s",start));
			start = start + strlen(start) + 1;
		}
		return list;
	}
	}
}
/*
 * dev_t di_prop_devt(di_prop_t prop);
 * #return the dev_t this property is associated.
 * #DDI_DEV_T_NONE for not property not assocated with any dev_t
 */

/*
 * minor - Basic type operations
 */

static PyObject* minor_new(PyTypeObject *type,PyObject *args,PyObject *kwds) {
	minorobj_t self = (minorobj_t) type->tp_alloc(type,0);
	if (self == NULL) {
		PyErr_NoMemory();
		return NULL;
	}
	self->minor = NULL;
	return (PyObject *)self;
}

static int minor_clear(minorobj_t self) {
	if (self != NULL)
		if (self -> minor != NULL)
			self -> minor = NULL;
	return 0;
}

static void minor_dealloc(minorobj_t self) {
	minor_clear(self);
	self->ob_type->tp_free((PyObject*)self);
}

static int minor_init(minorobj_t self,PyObject *args,PyObject *kwds) {
	PyObject *root = NULL;
	static char *kwlist[]={"minor",NULL};
	if (!PyArg_ParseTupleAndKeywords(args,kwds,"|O",kwlist,&root)) return -1;
	if (root) {
		self->minor = ((minorobj_t)root)->minor;
	}
	else {
		self->minor = NULL;
	}
	return 0;
}

static PyObject * minor_devfs_path(PyObject * self,PyObject *args) {
	di_minor_t minor = ((minorobj_t) self)->minor;
	if (!PyArg_Parse(args,"")) return NULL;

	if (minor != DI_MINOR_NIL) {
		char *dpath = di_devfs_minor_path(minor);
		PyObject *ret = Py_BuildValue("s",dpath);
		di_devfs_path_free(dpath);
		return ret;
	}
	else
		onError("cannot access node : DI_MINOR_NIL");
}

static PyObject * minor_name(PyObject * self,PyObject *args) {
	di_minor_t minor = ((minorobj_t) self)->minor;
	if (!PyArg_Parse(args,"")) return NULL;

	if (minor != DI_MINOR_NIL) {
		return Py_BuildValue("s",di_minor_name(minor));
	}
	else
		onError("cannot access node : DI_MINOR_NIL");
}

static PyObject * minor_spectype(PyObject * self,PyObject *args) {
	di_minor_t minor = ((minorobj_t) self)->minor;
	if (!PyArg_Parse(args,"")) return NULL;

	if (minor != DI_MINOR_NIL) {
		return Py_BuildValue("i",di_minor_spectype(minor));
	}
	else
		onError("cannot access node : DI_MINOR_NIL");
}

static PyObject * minor_nodetype(PyObject * self,PyObject *args) {
	di_minor_t minor = ((minorobj_t) self)->minor;
	if (!PyArg_Parse(args,"")) return NULL;

	if (minor != DI_MINOR_NIL) {
		return Py_BuildValue("s",di_minor_nodetype(minor));
	}
	else
		onError("cannot access node : DI_MINOR_NIL");
}

/*di_minor_devt, di_minor_nodetype, di_minor_type*/

static PyObject * minor_info(PyObject * self,PyObject *args) {
	di_minor_t minor = ((minorobj_t) self)->minor;
	PyObject * dict = PyDict_New();
	if (!PyArg_Parse(args,"")) return NULL;

	PyDict_SetItem(dict, Py_BuildValue("s","minor name"),minor_name(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","nodetype"),minor_nodetype(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","spectype"),minor_spectype(self,args));
	PyDict_SetItem(dict, Py_BuildValue("s","devfs path"),minor_devfs_path(self,args));

	return dict;
}
