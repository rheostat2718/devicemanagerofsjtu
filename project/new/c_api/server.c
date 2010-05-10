//gcc  -Wall -o server server.c `pkg-config gtk+-2.0 libnotify --libs --cflags`

#include <Python.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <door.h>
#include <pthread.h>

static void serv_proc(void * pcookie,
        char * argp,
        size_t argsz,
        door_desc_t *dp,
        uint_t ndesc);

void t_run();

char *error, *cmd;
int quit;
pthread_mutex_t run,result;

int main(int argc, char * argv[]){

    int fd;
    int tempfd;

    fd=door_create(serv_proc, NULL, 0);
    unlink("111") ; //delete this file if it already exists from a previous run
    tempfd=fopen("111","w"); //create the file associated with the door
    close (tempfd); //close the file before attaching it to fd

    chmod("111",0x777);

    fattach(fd, "111"); //associate door descriptor with an existing file

    sem_init(&run,0,1);
    sem_init(&result,0,1);

    sem_init(&quit,0,1);
    //sem_lock(&quit);
    quit=0;

    printf("server wait\n");
    sem_wait(&quit);
    unlink("111");
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
    //Py_Initialize();
    //PyRun_SimpleString("import sys,os");
    //PyRun_SimpleString("sys.path.append(os.getcwd())");
    //PyObject *ptr;
    //PyObject *pmod;
    //PyObject *pdict;
    char res[64]="NONE";

    //PyRun_SimpleString("print 'hello, in python'");


    if (strcmp(argp,"quit")==0){
        printf("quit=%d\n",quit);
        sem_post(&quit);
        printf("quit=%d\n",quit);
    } else {
        //pmod=PyImport_ImportModule("tools");
        //pdict=PyModule_GetDict(pmod);
        //
        printf("not quit\ncmd:%s\n",argp);
        if (strcmp(argp,"query")==0){
            printf("in query\n");
            if (error==100)
            {
                strcpy(res,"wait");
            }
            else if (error==0){
                strcpy(res,"succeeded");
            }
            else strcpy(res,"failed");

        }
        else if (strncmp(argp,"CMD:",4)==0){
            pthread_mutex_lock(&run);
            printf("%s\n",argp);
            cmd=strtok(argp,":");
            cmd=strtok(NULL, ":");
            //printf("in door server, run:%s\n",cmd);
            
            pthread_t thread;
            int tmp;
            
            if ((tmp=pthread_create(&thread,NULL,t_run,NULL))!=0)
            {
                strcpy(res,"failed");
                printf("error in running thread");
            }
            else
            {
                usleep(300);
                strcpy(res,"wait");
            }
            pthread_mutex_unlock(&run);
        }
        if (strcmp(argp,"reconf")==0){
            printf("reconfigure\n");

            int f=fopen("/reconfigure","w");
            close(f);
            if (chmod("/reconfigure",0x777)!=-1)
                strcpy(res,"succeeded");
            else
                strcpy(res,"failed");
        }
    }

    //if (res!=0)
    //    PyArg_Parse(ptr,"s",&res);
    //Py_Finalize();
    //printf("in door server %s\n", res);
    //
    printf("%s\n",res);
    if (door_return (res, sizeof(res), NULL, 0)==-1)
        printf("door_return failed\n");
}

void t_run(){
    pthread_mutex_lock(&result);
    printf("result=%d\n",result);
    printf("in t_run");
    error=100;
    error=system(cmd);
    pthread_mutex_unlock(&result);
    printf("result=%d\n",result);
}
