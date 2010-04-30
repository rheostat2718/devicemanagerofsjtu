CC=gcc
LD=ld
PYINC=/usr/include/python2.6
COMPOPT=-g -c -I$(PYINC) -fpic
LINKOPT=-shared -g

TODO:modulec.so;

all:TODO;

modulec.so:modulec.o
	$(LD) modulec.o $(LINKOPT) -o modulec.so
modulec.o:modulec.c
	$(CC) modulec.c $(COMPOPT)

clean:
	rm -f core *.o *.pyc *.c~ *.py~
cleanall:clean
	rm -f *.so
