#!/bin/bash

execs=("1dstrfind" "2dstrfind" "wraparound")
sources_c=( "${execs[@]/%/.c}" )
sources_s=( "${execs[@]/%/.s}" )

for cfile in "${execs[@]}"; do
	gcc "src/$cfile.c" -o "bin/$cfile" -Wall
	cp "src/$cfile.s" "bin/"
done

g++ "mars/checker.cpp" -o "bin/checker" -std=c++11
g++ "mars/generator.cpp" -o "bin/generator" -std=c++11
cp "mars/mars.jar" "bin/"


