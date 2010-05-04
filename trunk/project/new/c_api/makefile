CC=gcc
LD=gcc
PYINC=/usr/include/python2.4
COMPOPT=-g -c -I$(PYINC) -fpic
LINKOPT=-shared -g
PYTHON=/bin/python2.4

TODO:modulec.so;

all:TODO;

modulec.so:modulec.o
	$(LD) modulec.o $(LINKOPT) -o modulec.so
modulec.o:modulec.c
	$(CC) modulec.c $(COMPOPT)

test:modulectest;
modulectest:
	$(PYTHON) moduleTest.py 

clean:
	rm -f core *.o *.pyc *.c~ *.py~
cleanall:clean
	rm -f *.so
