CC=gcc
LD=ld
PYINC=/usr/include/python2.6
COMPOPT=-g -c -I$(PYINC) -fpic
LINKOPT=-shared -g

TODO:devicec.so modulec.so di.so;

devicec.so:devicec.o
	$(LD) devicec.o -ldevinfo $(LINKOPT) -o devicec.so
devicec.o:devicec.c
	$(CC) devicec.c $(COMPOPT)
modulec.so:modulec.o
	$(LD) modulec.o $(LINKOPT) -o modulec.so
modulec.o:modulec.c
	$(CC) modulec.c $(COMPOPT)
di.so:di.o
	$(LD) di.o -ldevinfo $(LINKOPT) -o di.so
di.o:di.c di.h
	$(CC) di.c $(COMPOPT)
	

clean:
	rm -f core *.o *.pyc *.c~ *.py~
cleanall:clean
	rm -f *.so
