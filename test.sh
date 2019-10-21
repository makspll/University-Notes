#!/bin/bash

st=0
en=20
execs=("1dstrfind" "2dstrfind" "wraparound")
exe=2
tests=0
ass=0
count=0

helpmess="
test.sh [-h|--help][-s|--start start_index][-e|--end end_index]
		[-t|--tests][-ta|--testass][-f|--file 1-3]
	 -h --help : prints this message 
	 -s --start index: program will start testing at specific index
	 -e --end index: program will finish at specific index inclusive
	 -t --test: program will use predefined tests to test the c program
		 tests should be included in tests/{dic/gri/out}/f<num>.txt
	 -ta --testass: tests assebly program againt tests
	 -f --file coursework file to use
		 1 1dstrfind
		 2 2dstrfind
		 3 wraparound
		 Made By Twoja stara company
"
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
	-h | --help )
		echo "$helpmess"
		exit
    ;;
	-s | --start )
		shift; st=$1
    ;;
	-e | --end )
		shift; en=$1
    ;;
	-t | --tests )
		tests=1
	;;
	-ta | --testass )
		tests=1
		ass=1
	;;
	-f | --file )
		shift; exe=$(($1-1))
	;;
	-g | --gen )
		tests=2
	;;
esac; shift; done

grid="2dgrid.txt"
testgrid="2d"
if (($exe == 0)); then
	grid="1dgrid.txt"
	testgrid="1d"
fi
if (($exe == 2)); then
	testgrid="wa"
fi

ex=${execs[$exe]}

# special case for generating
if (( $tests == 2)); then
	for ((i = $st; i <= en; i++)); do
		echo "$exe $i" | bin/generator "$grid" "dictionary.txt" 
		cp "dictionary.txt" "tests/dict/$testgrid/$i.txt"
		cp $grid "tests/grid/$testgrid/$i.txt"
#		echo "$i"
		bin/$ex 1>ou2
		cp "ou2" "tests/out/$testgrid/$i.txt"
		out=$(cat ou2)
		if [[ $out == "-1" ]]; then
			count=$(($count+1))
		fi
	done
	echo $count
	exit
fi

if (( $tests == 1 )); then
# check output based on give tests in tests/dict tests/grid/$grid$num tests/out
	for ((i = $st; i <= en; i++)); do
		cp "tests/dict/$testgrid/$i.txt" "dictionary.txt"
		cp "tests/grid/$testgrid/$i.txt" "$grid"
		cp "tests/out/$testgrid/$i.txt" "ou1"
		if (($ass ==1)); then
			java -jar bin/mars.jar sm me "bin/$ex.s" 1> ou2 2>/dev/null # can also use those instead but it's a lot slower
		else
			bin/$ex 2>/dev/null 1>ou2 
		fi
		out=$(bin/checker ou1 ou2)
		if (($st + 15 < $en)); then # if testing a lot of tests, print just falses and progress message to stderr
			if [[ $out != "True" ]]; then
				echo -e "False $i, dumping grid,dictionary to fails.txt\n"
				echo -e "program: $exe (0 = 1dstrfind, 1 = 2dstrfind, 2 = wraparound)\n.c or .s: $ass (0 = C, 1 = MIPS)\n" >> fails.txt
				echo -e "failed test $i \ngrid:\n" >> fails.txt
				cat $grid >> fails.txt
				echo -e "dicitonary:\n" >> fails.txt
				cat dictionary.txt >> fails.txt
			fi
			if (( $i % 10 == 0)); then
				>&2 echo "Went through $i"
			fi
		else
			echo "${out} $i"
		fi
	done
else
# check against the c files
	for ((i = $st; i <= en; i++)); do
		echo "$exe $i" | bin/generator "$grid" "dictionary.txt" 
		java -jar bin/mars.jar sm me "bin/$ex.s" 1> ou1 2>/dev/null 
		bin/$ex 2>/dev/null 1>ou2 
		out="$(bin/checker ou1 ou2)" 
		if (($st + 15 < $en)); then # if testing a lot of tests, print just falses and progress message to stderr
			if [[ $out != "True" ]]; then
				echo "False $i"
			fi
			if (( $i % 10 == 0)); then
				>&2 echo "Went through $i"
			fi
		else
			echo "${out} $i"
		fi
	done
fi

