#
# test for makefile
LINKOPTIONS = -g -ldevinfo
COMPILEOPTIONS = -g -c
COMPILER = gcc
all:exp1 exp2 exp3
exp1:exp1.o
	$(COMPILER) exp1.o $(LINKOPTIONS) -o exp1
exp1.o:exp1.c
	$(COMPILER) exp1.c $(COMPILEOPTIONS) exp1.c
exp2:exp2.o
	$(COMPILER) exp2.o $(LINKOPTIONS) -o exp2
exp2.o:exp2.c
	$(COMPILER) exp2.c $(COMPILEOPTIONS) exp2.c
exp3:exp3.o
	$(COMPILER) exp3.o $(LINKOPTIONS) -o exp3
exp3.o:exp3.c
	$(COMPILER) exp3.c $(COMPILEOPTIONS) exp3.c
clear:;
	rm exp1.o exp2.o exp3.o exp1 exp2 exp3

