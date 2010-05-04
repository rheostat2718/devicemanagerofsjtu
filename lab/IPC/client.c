#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <fcntl.h>
#include <door.h>
//#include "ssp.h" //Solaris stuff


int main(int argc, char* argv[]){
    int fd;
    int val; 
    long res; 
    door_arg_t door_args ={0};//zero all members
    fd=open(argv[1], O_RDWR);
    val=atoi(argv[2]);
    door_args.data_ptr=(char*)&val;
    door_args.data_size=sizeof (val);

    //skipping desc_ptr and desc_num. both were zero initialized 
    door_args.rbuf=(char*)&res; // the result will be written to rbuf
    door_args.rsize=sizeof(res);
    if(door_call(fd, &door_args)==0)
        printf("the result is: %ld\n", res);
    else
        printf("nothing!\n");
}
