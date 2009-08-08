CC=gcc
LD=ld
PYINC=/usr/include/python2.6
COMPOPT=-g -c -I$(PYINC) -fpic
LINKOPT=-shared -g

TODO:device.so modulec.so;

device.so:device.o
	$(LD) device.o -ldevinfo $(LINKOPT) -o device.so
device.o:device.c
	$(CC) device.c $(COMPOPT)
modulec.so:modulec.o
	$(LD) modulec.o $(LINKOPT) -o modulec.so
modulec.o:modulec.c
	$(CC) modulec.c $(COMPOPT)


clean:
	rm -f core *.o *.pyc
cleanall:clean
	rm -f *.so
