#!/bin/bash

COMMAND_1="./mkFit/mkFit --read --file-name simtracks_barrel_20x10k.bin --num-thr"
COMMAND_2="--build-std"

NUM_THREADS="10"
amplxe-cl -collect hotspots -r hs$NUM_THREADS $COMMAND_1 $NUM_THREADS $COMMAND_2

NUM_THREADS="20"
amplxe-cl -collect hotspots -r hs$NUM_THREADS $COMMAND_1 $NUM_THREADS $COMMAND_2

NUM_THREADS="30"
amplxe-cl -collect hotspots -r hs$NUM_THREADS $COMMAND_1 $NUM_THREADS $COMMAND_2

NUM_THREADS="40"
amplxe-cl -collect hotspots -r hs$NUM_THREADS $COMMAND_1 $NUM_THREADS $COMMAND_2

NUM_THREADS="50"
amplxe-cl -collect hotspots -r hs$NUM_THREADS $COMMAND_1 $NUM_THREADS $COMMAND_2

NUM_THREADS="60"
amplxe-cl -collect hotspots -r hs$NUM_THREADS $COMMAND_1 $NUM_THREADS $COMMAND_2

NUM_THREADS="70"
amplxe-cl -collect hotspots -r hs$NUM_THREADS $COMMAND_1 $NUM_THREADS $COMMAND_2

NUM_THREADS="80"
amplxe-cl -collect hotspots -r hs$NUM_THREADS $COMMAND_1 $NUM_THREADS $COMMAND_2

NUM_THREADS="90"
amplxe-cl -collect hotspots -r hs$NUM_THREADS $COMMAND_1 $NUM_THREADS $COMMAND_2

NUM_THREADS="100"
amplxe-cl -collect hotspots -r hs$NUM_THREADS $COMMAND_1 $NUM_THREADS $COMMAND_2

NUM_THREADS="120"
amplxe-cl -collect hotspots -r hs$NUM_THREADS $COMMAND_1 $NUM_THREADS $COMMAND_2

NUM_THREADS="110"
amplxe-cl -collect hotspots -r hs$NUM_THREADS $COMMAND_1 $NUM_THREADS $COMMAND_2

