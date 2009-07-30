#include <Python.h>
#include <string.h>
#include <sys/utsname.h>
#include <libdevinfo.h>

/*
 * define of getDeviceNodeName(node)
 * return a name of a node
 */
static PyObject *
getDeviceNodeName(PyObject *self, PyObject *args)
{
  int node;
  if (! PyArg_Parse(args, "(i)", &node))
    return NULL;
  else
  {
    return Py_BuildValue("s",di_node_name(node));
  }
}

static struct PyMethodDef getDeviceNodeName_methods[]=
{
  {"getDeviceNodeName",getDeviceNodeName,1},
  {NULL,NULL}
};

void initgetDeviceNodeName()
{
  (void) Py_InitModule("getDeviceNodeName",getDeviceNodeName_methods);
}
/*
 * define of getDeviceList()
 * return device list
 */

static int
listinit(int node, PyObject *list)
{
  PyList_Append(list, Py_BuildValue("i",node));
  return (DI_WALK_CONTINUE);
}

static PyObject *
getDeviceList(PyObject *self, PyObject *args)
{
  int root_node;
  extern void exit();

  if ((root_node=di_init("/", DINFOSUBTREE))==DI_NODE_NIL)
  {
    perror("di_init() failed\n");
    exit(1);
  }

  PyObject *list=PyList_New(0);

  (void) di_walk_node(root_node, DI_WALK_CLDFIRST, (void *)list, listinit);
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
