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

int main(int argc, char * argv[]){

    int fd;
    int tempfd;
    
    fd=door_create(serv_proc, NULL, 0);
    unlink("tmp_door") ; //delete this file if it already exists from a previous run
    tempfd=fopen("tmp_door","w"); //create the file associated with the door
    close (tempfd); //close the file before attaching it to fd

    fattach(fd, "tmp_door"); //associate door descriptor with an existing file

    while (1)
        pause();

    return 0;
}

static 
void serv_proc(void * pcookie, 
           char * argp, 
           size_t argsz, 
           door_desc_t *dp, 
           uint_t ndesc)
{
    printf("%s\n",argp);
    
    /*
     * your task
     */
    
    
    char res[64]="success";
    
    
    if (door_return (res, sizeof(res), NULL, 0)==-1)
        printf("door_return failure\n");
}

