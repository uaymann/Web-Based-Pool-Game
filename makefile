CC = clang
CFLAGS = -Wall -std=c99 -pedantic
SWIG = swig
PYTHON = python3.11

all: A2

clean:
	rm -f *.o *.so *.svg A2 phylib_wrap.c phylib.py

libphylib.so: phylib.o
	$(CC) phylib.o -shared -o libphylib.so -lm

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -fPIC -o phylib.o

phylib_wrap.c phylib.py: phylib.i
	$(SWIG) -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/$(PYTHON) -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o
	$(CC) $(CFLAGS) phylib_wrap.o -shared -L. -L/usr/lib/$(PYTHON) -l$(PYTHON) -lphylib -o _phylib.so

A2: libphylib.so _phylib.so

