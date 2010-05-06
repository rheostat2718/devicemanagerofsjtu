#include <Python.h>

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <fcntl.h>
#include <door.h>

static PyObject *
send(PyObject *self, PyObject *args){
    char *msg, res[64];
    if (! PyArg_Parse(args, "(s)", &msg))
        return NULL;

    int fd;

    door_arg_t door_args ={0};//zero all members

    fd=open("c_api/111", O_RDWR);
    door_args.data_ptr=msg;
    door_args.data_size=sizeof(msg)*strlen(msg);

    //skipping desc_ptr and desc_num. both were zero initialized
    door_args.rbuf=(char*)&res; // the result will be written to rbuf
    door_args.rsize=sizeof(res);
    if(door_call(fd, &door_args)==0)
    {
        return Py_BuildValue("s", res);
    }
    else
        printf("error: send nothing!\n");

    return Py_BuildValue("s", "nothing");
}

static struct PyMethodDef client_methods[]={
    {"send", send, 1},
    {NULL,NULL}
};

void initclient()
{
    (void) Py_InitModule("client", client_methods);
}

