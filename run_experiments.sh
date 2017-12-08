#!/bin/bash

#./mkFit/mkFit --num-tracks 5000 --num-events 10000 --write --file-name simtracks_barrel_large.bin

NT=10
#FILE=../mictest_sampling/simtracks_barrel_5g.bin
FILE=../mictest_sampling/simtracks_barrel_large.bin
#CMD=tau_exec -T tbb,serial -ebs ./mkFit/mkFit --read --file-name $FILE --num-thr $NT --fit-std-only --silent
CMD=./mkFit/mkFit\ --read\ --file-name\ $FILE\ --num-thr\ $NT\ --fit-std-only\ --silent

rm -r MULTI__*

export TAU_METRICS=TIME,PAPI_NATIVE_UOPS_RETIRED:SCALAR_SIMD,PAPI_NATIVE_UOPS_RETIRED:PACKED_SIMD
$CMD

export TAU_METRICS=TIME,PAPI_TOT_CYC
$CMD

export TAU_METRICS=TIME,PAPI_RES_STL
$CMD

export TAU_METRICS=TIME,PAPI_LST_INS
$CMD

export TAU_METRICS=TIME,PAPI_L1_TCM
$CMD

export TAU_METRICS=TIME,PAPI_NATIVE_LLC_MISSES,PAPI_NATIVE_LLC_REFERENCES
$CMD

