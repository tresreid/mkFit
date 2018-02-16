#!/bin/bash

#./mkFit/mkFit --num-tracks 5000 --num-events 10000 --write --file-name simtracks_barrel_large.bin

NT=10

rm -r MULTI__*

CMDp1=tau_exec\ -T\ papi,icpc,pdt,tbb,serial\ -ebs\ -ebs_period=10039 
CMDp2=./mkFit/mkFit\ --read\ --file-name\ simtracks_barrel_5k_tracks_10k_events.bin\ --num-thr\ $NT\ --fit-std-only\ --silent
#CMDp2=./mkFit/mkFit\ --read\ --file-name\ simtracks_barrel_20x10k.bin\ --num-thr\ $NT\ --fit-std-only\ --silent

export TAU_METRICS=TIME,PAPI_NATIVE_UOPS_RETIRED:SCALAR_SIMD,PAPI_NATIVE_UOPS_RETIRED:PACKED_SIMD
$CMDp1 $CMDp2
#$CMDp1 -ebs_source=PAPI_NATIVE_UOPS_RETIRED:PACKED_SIMD $CMDp2
#$CMDp1 -ebs_source=PAPI_NATIVE_UOPS_RETIRED:SCALAR_SIMD $CMDp2

export TAU_METRICS=TIME,PAPI_TOT_CYC,PAPI_TOT_INS,PAPI_L2_TCM
$CMDp1 $CMDp2
#$CMDp1 -ebs_source=PAPI_TOT_CYC $CMDp2
#$CMDp1 -ebs_source=PAPI_TOT_INS $CMDp2
#$CMDp1 -ebs_source=PAPI_TOT_TCM $CMDp2

export TAU_METRICS=TIME,PAPI_RES_STL,PAPI_L2_TCA
$CMDp1 $CMDp2
#$CMDp1 -ebs_source=PAPI_RES_STL $CMDp2
#$CMDp1 -ebs_source=PAPI_L2_TCA $CMDp2

export TAU_METRICS=TIME,PAPI_LST_INS
$CMDp1 $CMDp2
#$CMDp1 -ebs_source=PAPI_LST_INS $CMDp2

export TAU_METRICS=TIME,PAPI_L1_TCM
$CMDp1 $CMDp2
#$CMDp1 -ebs_source=PAPI_L1_TCM $CMDp2

export TAU_METRICS=TIME,PAPI_NATIVE_LLC_MISSES,PAPI_NATIVE_LLC_REFERENCES
$CMDp1 $CMDp2
#$CMDp1 -ebs_source=PAPI_NATIVE_LLC_MISSES $CMDp2
#$CMDp1 -ebs_source=PAPI_NATIVE_LLC_REFERENCES $CMDp2

