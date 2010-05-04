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
    int fd;
    int tempfd;
    //get descriptor and bind serv_proc to it
    
    fd=door_create(serv_proc, NULL, 0);
    unlink(argv[1]) ; //delete this file if it already exists from a previous run
    tempfd=fopen(argv[1],"w"); //create the file associated with the door
    close (tempfd); //close the file before attaching it to fd

    fattach(fd, argv[1]); //associate door descriptor with an existing file
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
    printf("hello in DOOR\n");
    int val = *((int *) argp); 
    long res=val*val;
    
    if (door_return ((char *) &res, sizeof(res), NULL, 0)==-1)
        printf("door_return failure\n");
}
