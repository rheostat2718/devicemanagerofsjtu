#include <Python.h>
#include <sys/modctl.h>
#include <stdio.h>
#include <string.h>

static PyObject * getModuleInfo(PyObject * self, PyObject *id) {
  int n,k = 0;
  struct modinfo mi;
  PyObject *info=PyDict_New();
  PyObject *sp_info=PyList_New(0);
  if (!PyArg_Parse(id,"(i)",&n)) return NULL;
  mi.mi_id = n;
  mi.mi_info = MI_INFO_ONE | MI_INFO_CNT | MI_INFO_NOBASE;
  mi.mi_nextid = n;
  if (modctl(MODINFO,n,&mi) < 0) return NULL;
  mi.mi_name[MODMAXNAMELEN-1] = '\0';
  PyDict_SetItem(info, Py_BuildValue("s","id"),Py_BuildValue("i",mi.mi_id));
  PyDict_SetItem(info, Py_BuildValue("s","LOADED"),Py_BuildValue("i",mi.mi_state & MI_LOADED));
  PyDict_SetItem(info, Py_BuildValue("s","INSTALLED"),Py_BuildValue("i",mi.mi_state & MI_INSTALLED));
  PyDict_SetItem(info,Py_BuildValue("s","loadcnt"),Py_BuildValue("i",mi.mi_loadcnt));
  PyDict_SetItem(info,Py_BuildValue("s","name"),Py_BuildValue("s",mi.mi_name));
  PyDict_SetItem(info,Py_BuildValue("s","size"),Py_BuildValue("l",mi.mi_size));
  PyDict_SetItem(info,Py_BuildValue("s","rev"),Py_BuildValue("i",mi.mi_rev));
/*FIXME: we do not need mi_base at all
  PyDict_SetItem(info,Py_BuildValue("s","addr"),Py_BuildValue("l",mi.mi_base));
  caddr_t addr;
 */
  for (;k<MODMAXLINK;k++) {
    if (mi.mi_msinfo[k].msi_linkinfo[0] == '\0') break;
    PyObject *msinfo=PyDict_New();
    mi.mi_msinfo[k].msi_linkinfo[MODMAXNAMELEN - 1] = '\0';
    PyDict_SetItem(msinfo,Py_BuildValue("s","linkinfo"),Py_BuildValue("s",mi.mi_msinfo[k].msi_linkinfo));
    PyDict_SetItem(msinfo,Py_BuildValue("s","p0"),Py_BuildValue("i",mi.mi_msinfo[k].msi_p0));
    PyList_Append(sp_info,msinfo);
  }
  k--;
  PyDict_SetItem(info,Py_BuildValue("s","infocnt"),Py_BuildValue("i",k));
  PyDict_SetItem(info,Py_BuildValue("s","specific_info"),sp_info);
  return info;
}

static PyObject * getModuleId(PyObject * self, PyObject *arg) {
  struct modinfo mi;
  int id= -1;
  char *name;
  if (!PyArg_Parse(arg,"(s)",&name)) return NULL;
  mi.mi_id = mi.mi_nextid = id;
  mi.mi_info = MI_INFO_ALL | MI_INFO_NOBASE;
  do {
    if (modctl(MODINFO, id, &mi) < 0) return Py_BuildValue("",id);
    id = mi.mi_id;
  } while (strcmp(name, mi.mi_name) != 0);
  return Py_BuildValue("i",id);
}

static PyObject * getModPath(PyObject *self, PyObject *arg) {
  char path[MAXPATHLEN];
  if (!PyArg_Parse(arg,"")) return NULL;
  if (modctl(MODGETPATH, NULL, path) != 0) return NULL;
  return Py_BuildValue("s",path);
}

static PyObject * getModPathLen(PyObject *self, PyObject *arg) {
  int len;
  if (!PyArg_Parse(arg,"")) return NULL;
  if (modctl(MODGETPATHLEN, NULL, &len) != 0) return NULL;
  return Py_BuildValue("i",len);
}

static PyObject * getMajorName(PyObject *self, PyObject *arg) {
    char name[64];
    int major;
    if (!PyArg_Parse(arg,"(i)",&major)) return NULL;
    if (modctl(MODGETNAME, name, 64, &major) != 0) return NULL;
    return Py_BuildValue("s",name);
}

//Return the last major number in the range of permissible major numbers.
static PyObject * getModReserve(PyObject *self, PyObject *arg) {
//FIXME:
  long max_dev = -1,id;
  if (!PyArg_Parse(arg,"(i)",&id)) return NULL;
  if (modctl(MODRESERVED, id, &max_dev) < 0) return NULL;
  return Py_BuildValue("l",max_dev);
}

static struct PyMethodDef modulec_methods[] = {
    {"getModuleInfo",getModuleInfo,1},
    {"getModuleId",getModuleId,1},
//TODO:FIXME    {"getModReserve",getModReserve,1},
    {"getModPath",getModPath,0},
    {"getModPathLen",getModPathLen,0},
//TODO:TEST IT    {"getMajorName",getMajorName,1},
    {NULL,NULL}
};

void initmodulec() {
  (void) Py_InitModule("modulec",modulec_methods);
}

