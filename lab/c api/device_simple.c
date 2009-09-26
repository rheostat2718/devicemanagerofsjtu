#include <Python.h>
#include <string.h>
#include <libdevinfo.h>

/*
 * define of getDeviceList()
 * return device list
 */

static int
listinit(di_node_t node, PyObject *list)
{
  PyList_Append(list, Py_BuildValue("i",node));
  return (DI_WALK_CONTINUE);
}

static PyObject *
getDeviceList(PyObject *self, PyObject *args)
{
  di_node_t root_node;
  extern void exit();

  if ((root_node=di_init("/", DINFOSUBTREE))==DI_NODE_NIL)
  {
    perror("di_init() failed\n");
    exit(1);
  }

  PyObject *list=PyList_New(0);
  PyList_Append(list, Py_BuildValue("i",root_node));
  //(void) di_walk_node(root_node, DI_WALK_CLDFIRST, list, listinit);

  di_fini(root_node);

  return list;
}

static struct PyMethodDef getDeviceList_methods[]=
{
  {"getDeviceList", getDeviceList, 1},
  {NULL, NULL}
};

void initgetDeviceList()
{
  (void) Py_InitModule("getDeviceList", getDeviceList_methods);
}
