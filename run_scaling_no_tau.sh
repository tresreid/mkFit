#!/bin/bash

#./mkFit/mkFit --num-tracks 5000 --num-events 10000 --write --file-name simtracks_barrel_large.bin

NT=10

CMDp2=./mkFit/mkFit\ --cmssw-n2seeds\ --input-file\ TTbar35PU-memoryFile.fv3.clean.writeAll.recT.072617.bin\ --build-ce\ --num-thr\ $NT\ --num-events\ 100

for i in {10..100..10}
do
NT=$i
./mkFit/mkFit --cmssw-n2seeds --input-file TTbar35PU-memoryFile.fv3.clean.writeAll.recT.072617.bin --build-ce --num-thr $NT --num-events 100 --silent 
echo
echo
done



