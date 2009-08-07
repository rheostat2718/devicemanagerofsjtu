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
  mi.mi_info = MI_INFO_ONE | MI_INFO_CNT | MI_INFO_NOBASE;
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
/*FIXME: we do not need mi_base at all
  PyDict_SetItem(info,Py_BuildValue("(s)","addr"),Py_BuildValue("(l)",mi.mi_base));
  caddr_t addr;
 */
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

static PyObject * getModuleId(PyObject * self, PyObject *driver_name) {
  struct modinfo modinfo;
  int id;
  char buf[MODMAXNAMELEN];
  if (!PyArg_Parse(driver_name,"(s)",&buf)) return NULL;
  modinfo.mi_id = -1;
  modinfo.mi_info = MI_INFO_ALL;
  do {
    if (modctl(MODINFO, 0, &modinfo) < 0) return NULL;
    id = modinfo.mi_id;
  } while (strcmp(buf, modinfo.mi_name) != 0);
  return Py_BuildValue("(i)",id);
}

//Return the last major number in the range of permissible major numbers.
static PyObject * getModReserve(PyObject *self, PyObject *arg) {
  int max_dev;
  if (!PyArg_Parse(arg,"()")) return NULL;
  if (modctl(MODRESERVED, NULL, &max_dev) < 0) return NULL;
  return Py_BuildValue("(i)",max_dev);
}

static PyObject * getModPath(PyObject *self, PyObject *arg) {
  char path[MAXPATHLEN];
  if (!PyArg_Parse(arg,"()")) return NULL;
  if (modctl(MODGETPATH, NULL, path) != 0) return NULL;
  return Py_BuildValue("(s)",path);
}

static PyObject * getModPathLen(PyObject *self, PyObject *arg) {
  int len;
  if (!PyArg_Parse(arg,"()")) return NULL;
  if (modctl(MODGETPATHLEN, NULL, &len) != 0) return NULL;
  return Py_BuildValue("(i)",len);
}

static PyObject * getMajorName(PyObject *self, PyObject *arg) {
    char name[64];
    int major;
    if (!PyArg_Parse(arg,"(i)",&major)) return NULL;
    if (modctl(MODGETNAME, name, 64, &major) != 0) return NULL;
    return Py_BuildValue("(s)",name);
}

static struct PyMethodDef module_methods[] = {
    {"getModuleInfo",getModuleInfo,1},
    ("getModuleId",getModuleId,1},
    ("getModReserve",getModReserve,0),
    ("getModPath",getModReserve,0),
    ("getModPathLen",getModReserve,0),
    ("getMajorName",getMajorName,1),
    {NULL,NULL}
};

void initmodule() {
  (void) Py_InitModule("module",module_methods);
}
