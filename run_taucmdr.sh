#!/bin/bash

#./mkFit/mkFit --num-tracks 5000 --num-events 10000 --write --file-name simtracks_barrel_large.bin

NT=10

EXP=multi

tau experiment select $EXP

#CMDp1=tau_exec\ -T\ papi,icpc,pdt,tbb,serial\ -ebs\ -ebs_period=10039
CMDp2=./mkFit/mkFit\ --read\ --file-name\ simtracks_barrel_5k_tracks_1k_events.bin\ --num-thr\ $NT\ --fit-std-only\ --silent

function run_stuff {

	tau experiment edit $EXP --measurement scalar_simd
	tau trial create $CMDp2

	tau experiment edit $EXP --measurement packed_simd
	tau trial create $CMDp2

	tau experiment edit $EXP --measurement tot_cyc
	tau trial create $CMDp2

	tau experiment edit $EXP --measurement tot_ins
	tau trial create $CMDp2

	tau experiment edit $EXP --measurement tcm2
	tau trial create $CMDp2

	tau experiment edit $EXP --measurement res_stl
	tau trial create $CMDp2

	tau experiment edit $EXP --measurement tca2
	tau trial create $CMDp2

	tau experiment edit $EXP --measurement lst
	tau trial create $CMDp2

	tau experiment edit $EXP --measurement tcm1
	tau trial create $CMDp2

	tau experiment edit $EXP --measurement llc_ref
	tau trial create $CMDp2

	tau experiment edit $EXP --measurement llc_miss
	tau trial create $CMDp2
}

run_stuff



