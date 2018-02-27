#!/bin/bash

#./mkFit/mkFit --num-tracks 5000 --num-events 10000 --write --file-name simtracks_barrel_large.bin



# parameters for mkFit
NT=10 # number of threads
NE=100 # number of simulated events
FILE=TTbar35PU-memoryFile.fv3.clean.writeAll.recT.072617.bin # input file name

# parameters for TAU
EXP=TTbar35_cache  # experiment name - must be created before running this script
tau experiment select $EXP # switch tau to this experiment

# command to execute the mkFit program
#    note the '\' before each space
#    also this must be redefined inside the loop to overwrite the variable as they vary
CMD=./mkFit/mkFit\ --cmssw-n2seeds\ --input-file\ $FILE\ --build-ce\ --num-thr\ $NT\ --num-events\ $NE


#measure_list=(tlb_dm)
measure_list=(tlb_dm br_ins br_cn br_ucn br_msp scalar_simd packed_simd tot_cyc tot_ins tcm2 res_stl tca2 lst tcm1 llc_ref llc_miss)
function run_trials {

	for i in ${measure_list[@]}; do
		tau experiment edit $EXP --measurement $i
		tau trial create $CMD
	done

}

for n in {0..3}; do
run_trials
done

FILE=TTbar70PU-memoryFile.fv3.clean.writeAll.recT.072617.bin
EXP=TTbar70_cache
CMD=./mkFit/mkFit\ --cmssw-n2seeds\ --input-file\ $FILE\ --build-ce\ --num-thr\ $NT\ --num-events\ $NE
tau experiment select $EXP

for n in {0..3}; do
run_trials
done

