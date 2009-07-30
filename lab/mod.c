#include <sys/modctl.h>
#include <sys/errno.h>
#include <stdio.h>
//what return value represents an error?
void modload(char *modpath) {//never use_path
	if (modctl(MODLOAD,0,modpath, &id) != 0) perror("modctl : MODLOAD")
	else return id
}
void modunload(int id) {
	if (modctl(MODUNLOAD,id) < 0) perror("modctl : MODUNLOAD")
}
struct ? modinfo(int id) {
	int n=0;
	struct modinfo mi;
	struct ? d;
/*typedef ? {
bool load
bool install
int id
int loadcnt
int rev
size_t size
const char* name
caddr_t addr
struct modspecific_info* info
int linkcnt
}*/
	mi.mi_id = id;
	mi.mi_info = MI_INFO_ONE | MI_INFO_CNT;
	mi.mi_nextid = id;
	if (modctl(MODINFO,id,&mi) < 0) perror("modctl: MODINFO");
	mi.mi_name[MODMAXNAMELEN -1] ='\0';
	d.id = mi.mi_id;
	d.load = mi.mi_state & MI_LOADED;
	d.install = mi.mi_state & MI_INSTALLED;
	d.loadcnt = mi.mi_loadcnt;
	d.name = mi.mi_name;
	d.size = mi.mi_size;
	d.rev = mi.mi_rev;
	d.addr = mi.mi_base;
	d.linkcnt = 0
	for (;d.linkcnt<MODMAXLINK;d.linkcnt++) {
		if (mi.mi_msinfo[n].msi_linkinfo[0] == '\0') break;
		mi.mi_msinfo[n].msi_linkinfo[MODMAXNAMELEN - 1] = '\0';
		d.info[n].msi_p0 = mi.mi_msinfo[n].msi_p0;
		d.info[n].msi_linkinfo = mi.mi_msinfo[n].msi_linkinfo;
	}
	d.linkcnt--;
}
int modreserve(void) {
	int max_dev;
	if (modctl(MODRESERVED, NULL, &max_dev) < 0) perror("modctl: MODRESERVED");
	return max_dev;
}
void modgetpath(char *path) {
	if (modctl(MODGETPATH, NULL, path) != 0) perror("modctl: MODGETPATH");
}

//following file from add_rem
void get_modid(char *driver_name, int *mod)
{
	struct modinfo	modinfo;
	modinfo.mi_id = -1;
	modinfo.mi_info = MI_INFO_ALL;
	do {
		if (modctl(MODINFO, 0, &modinfo) < 0) {
			*mod = -1;
			return;
		}
		*mod = modinfo.mi_id;
	} while (strcmp(driver_name, modinfo.mi_name) != 0);
}

