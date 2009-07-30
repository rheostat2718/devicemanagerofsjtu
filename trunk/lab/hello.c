#include <Python.h>
#include <string.h>

static PyObject*
message(PyObject *self, PyObject *args)
{
	char *fromPython, result[64];
	if (! PyArg_Parse(args, "(s)", &fromPython))
		return NULL;
	else
	{
		strcpy(result, "Hello, ");
		strcat(result, fromPython);
		return Py_BuildValue("s", result);
	}
}

static struct PyMethodDef hell_methods[]=
{
	{"message",message,1},
	{NULL,NULL}
};

void inithello()
{
	(void)Py_InitModule("hello", hello_methods);
}