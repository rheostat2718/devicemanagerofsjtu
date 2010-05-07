//gcc  -Wall -o server server.c `pkg-config gtk+-2.0 libnotify --libs --cflags`

#include <Python.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <door.h>

static void serv_proc(void * pcookie,
        char * argp,
        size_t argsz,
        door_desc_t *dp,
        uint_t ndesc);

int quit;

int main(int argc, char * argv[]){

    int fd;
    int tempfd;

    fd=door_create(serv_proc, NULL, 0);
    unlink("111") ; //delete this file if it already exists from a previous run
    tempfd=fopen("111","w"); //create the file associated with the door
    close (tempfd); //close the file before attaching it to fd

    chmod("111",0x777);

    fattach(fd, "111"); //associate door descriptor with an existing file

    sem_init(&quit,0,1);

    quit=0;

    printf("server wait\n");
    sem_wait(&quit);

    printf("server quit\n");
    //
    //

    return 0;
}

static
void serv_proc(void * pcookie,
           char * argp,
           size_t argsz,
           door_desc_t *dp,
           uint_t ndesc)
{
    Py_Initialize();
    PyRun_SimpleString("import sys,os");
    PyRun_SimpleString("sys.path.append(os.getcwd())");
    PyObject *ptr;
    PyObject *pmod;
    PyObject *pdict;

    PyRun_SimpleString("print 'hello, in python'");

    if (strcmp(argp,"quit")==0){
        printf("quit=%d\n",quit);
        sem_post(&quit);
        printf("quit=%d\n",quit);
    } else {
        pmod=PyImport_ImportModule("tools");
        pdict=PyModule_GetDict(pmod);

        if (strcmp(argp,"reconf")==0){

        }
        printf("%s\n", argp);
    }

    char res[64]="success";
    //PyArg_Parse(ptr,"s",&res);
    Py_Finalize();
    //printf("in door server %s\n", res);
    //
    printf("%s\n",res);
    if (door_return (res, sizeof(res), NULL, 0)==-1)
        printf("door_return failure\n");
}

