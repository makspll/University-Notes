ghc -prof -fprof-auto -rtsopts -Wall Inf2d1.hs -o main
./main +RTS -p -h
hp2ps -d -c main.hp
gv main.ps -orientation=SEASCAPE