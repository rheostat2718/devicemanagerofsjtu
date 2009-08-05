#include <Python.h>
#include <stdio.h>
#include <sys/utsname.h>
#include <libdevinfo.h>

/*
 * define of getDeviceList()
 * return device list
 */

static int addToList(di_node_t node, PyObject *list) {
  PyList_Append(list, Py_BuildValue("s",di_node_name(node)));
  return (DI_WALK_CONTINUE);
}

static PyObject * getDeviceList(PyObject *self, PyObject *args) {
  di_node_t root_node;
  if ((root_node=di_init("/", DINFOSUBTREE))==DI_NODE_NIL) return NULL;
  PyObject *list=PyList_New(0);
  (void) di_walk_node(root_node, DI_WALK_CLDFIRST, (void *)list, addToList);
  di_fini(root_node);
  return list;
}

static struct PyMethodDef device_methods[]= {
  {"getDeviceList", getDeviceList, 0},
  {NULL, NULL}
};

void initgetDeviceList() {
  (void) Py_InitModule("device", device_methods);
}
