COMPILER = gcc
PYLIB = /usr/bin
PYINC = /usr/include/python2.4
PYOPT = -I$(PYINC) -shared -L$(PYLIB) -lpython2.4

hello.so: hello.c
	$(COMPILER) hello.c $(PYOPT) -g -o hello.so
device.so: device.c
	$(COMPILER) device.c -ldevinfo $(PYOPT) -g -o device.so
clean:
	rm -f core *.o	