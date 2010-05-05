//gcc  -Wall -o notify notify.c `pkg-config gtk+-2.0 libnotify --libs --cflags`


#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <door.h>
#include <gtk/gtk.h>
#include <libnotify/notify.h>
//#include "ssp.h" //Solaris stuff

static void serv_proc(void * pcookie, 
        char * argp, 
        size_t argsz, 
        door_desc_t *dp, 
        uint_t ndesc);

void on_status_icon(GtkStatusIcon *icon, char *title, char *info);

int main(int argc, char * argv[]){
    gtk_init(&argc, &argv);

    int fd;
    int tempfd;
    //get descriptor and bind serv_proc to it
    
    fd=door_create(serv_proc, NULL, 0);
    unlink("tmp_door") ; //delete this file if it already exists from a previous run
    tempfd=fopen("tmp_door","w"); //create the file associated with the door
    close (tempfd); //close the file before attaching it to fd

    fattach(fd, "tmp_door"); //associate door descriptor with an existing file

    GtkStatusIcon *icon;

    if (!notify_init("notify"))
        g_warning("failed  to init notify");

    icon=gtk_status_icon_new_from_stock(GTK_STOCK_INFO);

    gtk_main();
    return 0;
}
i
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

}

void
on_status_icon(GtkStatusIcon *icon, char *title, char *info)
{
    NotifyNotification *tray=notify_notification_new_with_status_icon(title, info, GTK_STOCK_INFO, icon);
    notify_notification_show(tray, NULL);
}
