#!/bin/bash

#./mkFit/mkFit --num-tracks 5000 --num-events 10000 --write --file-name simtracks_barrel_large.bin

NT=10
FILE=simtracks_barrel_20x10k.bin

rm -r MULTI__*

export TAU_METRICS=TIME,PAPI_NATIVE_UOPS_RETIRED:SCALAR_SIMD,PAPI_NATIVE_UOPS_RETIRED:PACKED_SIMD
tau_exec -T tbb,serial -ebs ./mkFit/mkFit --read --file-name $FILE --num-thr $NT --fit-std-only --silent

export TAU_METRICS=TIME,PAPI_TOT_CYC
tau_exec -T tbb,serial -ebs ./mkFit/mkFit --read --file-name $FILE --num-thr $NT  --fit-std-only --silent

export TAU_METRICS=TIME,PAPI_RES_STL
tau_exec -T tbb,serial -ebs ./mkFit/mkFit --read --file-name $FILE --num-thr $NT --fit-std-only --silent

export TAU_METRICS=TIME,PAPI_LST_INS
tau_exec -T tbb,serial -ebs ./mkFit/mkFit --read --file-name $FILE --num-thr $NT --fit-std-only --silent

export TAU_METRICS=TIME,PAPI_L1_TCM
tau_exec -T tbb,serial -ebs ./mkFit/mkFit --read --file-name $FILE --num-thr $NT --fit-std-only --silent

export TAU_METRICS=TIME,PAPI_NATIVE_LLC_MISSES,PAPI_NATIVE_LLC_REFERENCES
tau_exec -T tbb,serial -ebs ./mkFit/mkFit --read --file-name $FILE --num-thr $NT --fit-std-only --silent
