#include <stdio.h>
#include <libdevinfo.h>
#include <sys/utsname.h>

static int
prt_nodename(di_node_t node, int i)
{
  printf("%d :%s\n", i, di_node_name(node));
  return (DI_WALK_CONTINUE);
}

int
main(void)
{
  di_node_t root_node;
  extern void exit();

  if ((root_node=di_init("/", DINFOSUBTREE)) == DI_NODE_NIL)
  {
    perror("di_init() failed\n");
    exit(1);
  }

  di_walk_node(root_node, DI_WALK_CLDFIRST, 0, prt_nodename);
  di_fini(root_node);
  return 0;
}
