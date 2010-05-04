#include <Python.h>

#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <door.h>
//#include "ssp.h" //Solaris stuff

static void serv_proc(void * pcookie, 
        char * argp, 
        size_t argsz, 
        door_desc_t *dp, 
        uint_t ndesc);

int main(int argc, char * argv[]){
    Py_Initialize();

    PyRun_SimpleString("print 'in python'");

    int fd;
    int tempfd;
    //get descriptor and bind serv_proc to it
    
    fd=door_create(serv_proc, NULL, 0);
    unlink("tmp_door") ; //delete this file if it already exists from a previous run
    tempfd=fopen("tmp_door","w"); //create the file associated with the door
    close (tempfd); //close the file before attaching it to fd

    fattach(fd, "tmp_door"); //associate door descriptor with an existing file
    while(1)
        pause(); //do nothing; the real work is implemented in the server threads
}

static 
void serv_proc(void * pcookie, 
           char * argp, 
           size_t argsz, 
           door_desc_t *dp, 
           uint_t ndesc)
{
    printf("%s\n",argp);
    char res[64]="success";
    if (door_return (res, sizeof(res), NULL, 0)==-1)
        printf("door_return failure\n");

    PyRun_SimpleString("print 'in python'");
}
