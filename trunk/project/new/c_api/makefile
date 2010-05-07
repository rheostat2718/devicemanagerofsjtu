CC=gcc
LD=gcc
PYINC=/usr/include/python2.4
COMPOPT=-g -c -I$(PYINC) -fpic
LINKOPT=-shared -g
PYTHON=/bin/python2.4
PYLIB=/usr/bin

TODO: modulec.so client.so server;

all:TODO;

modulec.so:modulec.o
	$(LD) modulec.o $(LINKOPT) -o modulec.so

modulec.o:modulec.c
	$(CC) modulec.c $(COMPOPT)

client.so:client.o
	$(LD) client.o $(LINKOPT) -o client.so

client.o:client.c
	$(CC) client.c $(COMPOPT) -o client.o

server:server.o
	gcc server.o -L/usr/include/python2.4 -lpython2.4 -g -o server

server.o:
	gcc server.c -c -g -I/usr/include/python2.4

test:modulectest;

modulectest:
	$(PYTHON) moduleTest.py

clean:
	rm -f core *.o *.pyc *.c~ *.py~

cleanall:clean
	rm -f *.so server
