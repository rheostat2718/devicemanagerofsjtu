CC=gcc
LD=ld
PYINC=/usr/include/python2.6
COMPOPT=-g -c -I$(PYINC) -fpic
LINKOPT=-shared -g

TODO:device.so;

device.so:device.o
	$(LD) device.o -ldevinfo $(LINKOPT) -o device.so
device.o:device.c
	$(CC) device.c $(COMPOPT)
mod.so:mod.o
	$(LD) mod.o $(LINKOPT) -o mod.so
mod.o:mod.c
	$(CC) mod.c $(COMPOPT)


clean:
	rm -f core *.o
cleanall:clean
	rm -f *.so
