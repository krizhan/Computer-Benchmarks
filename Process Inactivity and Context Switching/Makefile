CC = gcc
CC_FLAGS = -O2 -Wall -g

all:	partA1 partA2

tsc.o:	tsc.c tsc.h
	$(CC) $(CC_FLAGS) -c -o $(@) tsc.c

partA1:	tsc.o partA1.c common.c
	$(CC) $(CC_FLAGS) -o partA1 tsc.o partA1.c common.c

partA2:	tsc.o partA2.c common.c
	$(CC) $(CC_FLAGS) -o partA2 tsc.o partA2.c common.c

clean:	
	rm -f *.o *~ partA1 partA2
