#!/bin/bash

#./mkFit/mkFit --num-tracks 5000 --num-events 10000 --write --file-name simtracks_barrel_large.bin

NT=10 # number of threads
NE=10 # number of simulated events
EXP=event_scaling_TTbar35_cache
FILE=TTbar35PU-memoryFile.fv3.clean.writeAll.recT.072617.bin

tau experiment select $EXP

CMD=./mkFit/mkFit\ --cmssw-n2seeds\ --input-file\ $FILE\ --build-ce\ --num-thr\ $NT\ --num-events\ $NE


#measure_list=(tlb_dm)
measure_list=(tlb_dm scalar_simd packed_simd tot_cyc tot_ins tcm2 res_stl tca2 lst tcm1 llc_ref llc_miss br_ins br_cn br_ucn br_msp)

function run_trials {

        for i in ${measure_list[@]}; do
                tau experiment edit $EXP --measurement $i
                tau trial create $CMD
        done

}



for i in {10..100..10}
do
NE=$i
CMD=./mkFit/mkFit\ --cmssw-n2seeds\ --input-file\ $FILE\ --build-ce\ --num-thr\ $NT\ --num-events\ $NE
run_trials
run_trials
done

FILE=TTbar70PU-memoryFile.fv3.clean.writeAll.recT.072617.bin
EXP=event_scaling_TTbar70_cache
CMD=./mkFit/mkFit\ --cmssw-n2seeds\ --input-file\ $FILE\ --build-ce\ --num-thr\ $NT\ --num-events\ $NE
tau experiment select $EXP


for i in {10..100..10}
do
NE=$i
CMD=./mkFit/mkFit\ --cmssw-n2seeds\ --input-file\ $FILE\ --build-ce\ --num-thr\ $NT\ --num-events\ $NE
run_trials
run_trials
done




