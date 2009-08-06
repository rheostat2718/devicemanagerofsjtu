#include <Python.h>
#include <sys/modctl.h>
#include <stdio.h>

static PyObject * getModuleInfo(PyObject * self, PyObject *id) {
  int n,k = 0;
  struct modinfo mi;
  PyObject *info=PyDict_New(0);
  PyObject *sp_info=PyList_New(0);
  if (!PyArg_Parse(id,"(i)",&n)) return NULL;
  mi.mi_id = n;
  mi.mi_info = MI_INFO_ONE | MI_INFO_CNT;
  mi.mi_nextid = n;
  if (modctl(MODINFO,n,&mi) < 0) return NULL;
  mi.mi_name[MODMAXNAMELEN-1] = '\0';
  PyDict_SetItem(info, Py_BuildValue("(s)","id"),Py_BuildValue("(i)",mi.mi_id));
  PyDict_SetItem(info, Py_BuildValue("(s)","LOADED"),Py_BuildValue("(i)",mi.mi_state & MI_LOADED));
  PyDict_SetItem(info, Py_BuildValue("(s)","INSTALLED"),Py_BuildValue("(i)",mi.mi_state & MI_INSTALLED));
  PyDict_SetItem(info,Py_BuildValue("(s)","loadcnt"),Py_BuildValue("(i)",mi.mi_loadcnt));
  PyDict_SetItem(info,Py_BuildValue("(s)","name"),Py_BuildValue("(s)",mi.mi_name));
  PyDict_SetItem(info,Py_BuildValue("(s)","size"),Py_BuildValue("(l)",mi.mi_size));
  PyDict_SetItem(info,Py_BuildValue("(s)","rev"),Py_BuildValue("(i)",mi.mi_rev));
  PyDict_SetItem(info,Py_BuildValue("(s)","addr"),Py_BuildValue("(l)",mi.mi_base));
//FIXME: caddr_t addr;
  for (;k<MODMAXLINK;k++) {
    if (mi.mi_msinfo[k].msi_linkinfo[0] == '\0') break;
    PyObject *msinfo=PyDict_New(0);
    mi.mi_msinfo[n].msi_linkinfo[MODMAXNAMELEN - 1] = '\0';
    PyDict_SetItem(msinfo,Py_BuildValue("(s)","linkinfo"),Py_BuildValue("(s)",mi.mi_msinfo[n].msi_linkinfo));
    PyDict_SetItem(msinfo,Py_BuildValue("(s)","p0"),Py_BuildValue("(s)",mi.mi_msinfo[n].msi_p0));
    PyList_Append(sp_info,msinfo);
  }
  k--;
  PyDict_SetItem(info,Py_BuildValue("(s)","infocnt"),Py_BuildValue("(i)",k));
  PyDict_SetItem(info,Py_BuildValue("(s)","specific_info"),sp_info);
  return info;
}


static struct PyMethodDef module_methods[] = {
    {"getModuleInfo",getModuleInfo,1},
    {NULL,NULL}
};

void initmodule() {
  (void) Py_InitModule("module",module_methods);
}
}
