#!/bin/bash

#tests all files against pre-calculated test outputs and dumps the output to testlogs.txt

. ./setup.sh
"" > fails.txt

echo "testing c files\n" 

echo -e "1dstrfind.c\n"
. ./test.sh -e 600 -t -f 1

echo -e "2dstrfind.c\n"
. ./test.sh -e 600 -t -f 2

echo -e "wraparound.c\n" 
. ./test.sh -e 600 -t -f 3

echo -e "testing MIPS files\n" 

echo -e "1dstrfind.s\n"
. ./test.sh -e 600 -t -ta -f 1

echo -e "2dstrfind.s\n" 
. ./test.sh -e 600 -t -ta -f 2

echo -e "wraparound.s\n" 
. ./test.sh -e 600 -t -ta -f 3

echo -e "tests completed\n"

