#! /bin/bash

###########
## Input ##
###########

ben_arch=SKL-SP

###################
## Configuration ##
###################

## Source environment and common variables
source xeon_scripts/common-variables.sh ${suite}
source xeon_scripts/init-env.sh

## Platform specific settings
if [[ "${ben_arch}" == "SNB" ]]
then
    mOpt="-j 12"
    dir=/data2/nfsmic/slava77/samples
    maxth=24
    maxvu=8
    declare -a nths=("1" "2" "4" "6" "8" "12" "16" "20" "24")
    declare -a nvus=("1" "2" "4" "8")
    declare -a nevs=("1" "2" "4" "8" "12")
elif [[ "${ben_arch}" == "KNL" ]]
then
    mOpt="-j 64 AVX_512:=1"
    dir=/data1/work/slava77/analysis/CMSSW_9_1_0_pre1-tkNtuple/run1000
    maxth=256
    maxvu=16
    declare -a nths=("1" "2" "4" "8" "16" "32" "64" "96" "128" "160" "192" "224" "256")
    declare -a nvus=("1" "2" "4" "8" "16")
    declare -a nevs=("1" "2" "4" "8" "16" "32" "64" "128")
elif [[ "${ben_arch}" == "SKL-SP" ]]
then
    # build_type="build-ce"
    build_type="build-std"
    mOpt="-j 32 AVX_512:=1"
    dir=/data2/slava77/samples
    out_dir=sky_mthr_TTbar7
    maxth=64
    maxvu=16
    # declare -a nths=("1" "2" "10")
    declare -a nths=("5")
    declare -a nvus=("16")
    # declare -a nvus=("1" "2" "4" "8" "16")
    declare -a nevs=("1" "2" "4" "8" "16" "32" "64")
    # declare -a metrics=("PAPI_VEC_SP" "PAPI_SP_OPS" "PAPI_TOT_CYC")
    # declare -a metrics=("PAPI_L1_TCM" "PAPI_LST_INS")
    # declare -a metrics=("PAPI_TOT_CYC")
    declare -a metrics=("PAPI_TOT_CYC" "PAPI_L2_TCM" "PAPI_L2_TCA")
    # declare -a metrics=("PAPI_TOT_CYC")
    # declare -a metrics=("PAPI_LST_INS" "PAPI_L1_TCM" "PAPI_L2_TCA" "PAPI_L2_TCM" "PAPI_L3_TCA" "PAPI_L3_TCM" "PAPI_VEC_SP" "PAPI_SP_OPS" "PAPI_NATIVE_FP_ARITH:512B_PACKED_SINGLE")
    # declare -a metrics=("PAPI_VEC_SP" "PAPI_VEC_DP" "PAPI_SP_OPS" "PAPI_DP_OPS" "PAPI_TOT_CYC" "PAPI_L1_DCM" "PAPI_LST_INS")
else 
    echo ${ben_arch} "is not a valid architecture! Exiting..."
    exit
fi

## Common file setup
subdir=input_files
#file=memoryFile.fv3.clean.writeAll.recT.072617.bin
#file=10muEtaLT06Pt1to10_memoryFile.fv3.clean.writeAll.recT.072617.bin
# file=10muPt0p5to10HS_memoryFile.fv3.clean.writeAll.recT.072617.bin
file=TTbar70PU-memoryFile.fv3.clean.writeAll.recT.072617.bin
nevents=100000

## Common executable setup
minth=10
minvu=1
seeds="--cmssw-n2seeds"
exe="./mkFit/mkFit ${seeds} --input-file ${subdir}/${file}"

tau_exe="tau_exec -ebs -T serial,icpc,papi,tbb "

## Common output setup
dump=DumpForPlots
base=${ben_arch}_${sample}

####################
## Run Benchmarks ##
####################

## compile with appropriate options
make distclean ${mOpt}
make ${mOpt}

mkdir ${out_dir}

## Vectorization Benchmarks  nvu = num vector units?
for nvu in "${nvus[@]}"
do
    for minth in "${nths[@]}"
    do
        make clean ${mOpt}
        make ${mOpt} USE_INTRINSICS:=-DMPT_SIZE=${nvu}

        ## Common base executable
        oBase=${base}
        bExe="${tau_exe} ${exe} --${build_type} --silent --num-thr ${minth} --num-events ${nevents}"
        
        tau_dir=TAU__${oBase}_NVU${nvu}_NTH${minth}_${build_type}
        # mkdir ${tau_dir}
        for metric in "${metrics[@]}"
        do    
            #mkdir ${tau_dir}/${metric}
            export TAU_METRICS=TIME,${metric}
            ## Building-only benchmark
            echo "${oBase}: Benchmark [nTH:${minth}, nVU:${nvu}]"
            echo ${bExe} #> log_${metric}_${oBase}_NVU${nvu}_NTH${minth}_${build_type}.txt
            mkdir ${out_dir}/${tau_dir}_${metric}
            mv MULTI__* ${out_dir}/${tau_dir}_${metric}
        done
    done
done

## Final cleanup
make distclean ${mOpt}
