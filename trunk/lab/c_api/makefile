CC=gcc
LD=ld
PYINC=/usr/include/python2.6
COMPOPT=-g -c -I$(PYINC) -fpic
LINKOPT=-shared -g

TODO:devicec.so modulec.so;

devicec.so:devicec.o
	$(LD) devicec.o -ldevinfo $(LINKOPT) -o devicec.so
devicec.o:devicec.c
	$(CC) devicec.c $(COMPOPT)
modulec.so:modulec.o
	$(LD) modulec.o $(LINKOPT) -o modulec.so
modulec.o:modulec.c
	$(CC) modulec.c $(COMPOPT)


clean:
	rm -f core *.o *.pyc *.c~ *.py~
cleanall:clean
	rm -f *.so
