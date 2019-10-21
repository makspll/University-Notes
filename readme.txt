ALL CREDITS FOR TESTS TO MICHAL
all i did was create an autorunner for his tests, and added a grid/dictionary dump on fail functionality

to run

bash runtests.sh
under the hood this just runs test.sh with pre selected flags
if you want to just run a single file test
use
./setup.sh
./test.sh -h (for help panel)

for single file tests just run:
C files:
./test.sh -e 600 -t -f <1,2 or 3 here>
MIPS files:
./test.sh -e 600 -t -ta -f <1,2 or 3 here>
where -f 1,2,3 specifies the file to test (1-1dstrfind 2-2dstrfind 3-wraparound)
that's it

IT WILL CREATE MASSIVE FILES IF YOU FAIL ALL TESTS

the tests are not guaranteed to be 100% encompassing or correct (based on michals program) however a lot of people have checked them and it seems they work nicely.

WE TAKE NO RESPONSIBILITY FOR THEM FAILING YOU 
