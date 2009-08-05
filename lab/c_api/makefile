CC=gcc
LD=ld
PYINC=/usr/include/python2.6
COMPOPT=-g -c -I$(PYINC) 
LINKOPT=-fpic -g

TODO: device.so

device.so:device.o
	$(LD) hello.o $(LINKOPT) -ldevinfo -o hello.so
device.o:device.c
	$(CC) hello.c $(COMPOPT)

clean:
	rm -f core *.o
cleanall:
	rm -f *.so