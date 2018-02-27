#!/bin/python

'''
This is some trash to run scaling experiments on the mictest program
it puts them in the .tau/mictest_sampling/manual_scaling_TTbar35_cache' directory
or ...TTbar70_cache
'''


ENV  = 'export TAU_MAKEFILE=/home/users/gravelle/taucmdr-enterprise-2/system/tau/tau-2.27/x86_64/lib/Makefile.tau-93948b87-icpc-papi-tbb;\n'
ENV += 'export TAU_DIR=/home/users/gravelle/taucmdr-enterprise-2/system/tau/tau-2.27;\n'
ENV += 'export PATH=$TAU_DIR/x86_64/bin:$PATH\n'


DIR  = '.tau/mictest_sampling/'
FILE = 'TTbar35PU-memoryFile.fv3.clean.writeAll.recT.072617.bin'
CMD  = './mkFit/mkFit --cmssw-n2seeds --input-file {:s} --build-ce --num-thr {:d} --num-events {:d}'

TAU_METRIC = 'export TAU_METRICS=TIME,{}\n'
TAU = 'tau_exec -T 93948b87,tbb,papi,serial,icpc -ebs {:s}'

NUM_RUNS = 1
THREAD_LIST = [2, 4, 8, 16, 32, 48, 64, 80, 96]
NUM_EVENTS=100


print ENV
print CMD.format(FILE, 0, 0)

EXP_LIST = ['manual_scaling_TTbar35_cache', 'manual_scaling_TTbar70_cache']


METRIC_LIST = ['PAPI_TLB_DM', \
'PAPI_BR_INS', 'PAPI_BR_CN', 'PAPI_BR_UCN', 'PAPI_BR_MSP',\
'PAPI_NATIVE_UOPS_RETIRED:SCALAR_SIMD','PAPI_NATIVE_UOPS_RETIRED:PACKED_SIMD',\
'PAPI_TOT_CYC','PAPI_TOT_INS',\
'PAPI_L2_TCM', 'PAPI_L2_TCA',\
'PAPI_RES_STL',\
'PAPI_LST_INS', 'PAPI_L1_TCM',\
'PAPI_NATIVE_LLC_REFERENCES','PAPI_NATIVE_LLC_MISSES']

def run_trial(exp_name):
	'''
	exp_name is the name of the mimiced taucmdr experiment
	it will be used as the subdirectory under DIR
	it will be sompletely overwritten so don't leave important things there
	'''

	#TODO 'rm -rf' + DIR + exp_name

	trial_count = 0

	for m in METRIC_LIST:
		print TAU_METRIC.format(m)

		for n in THREAD_LIST:
			for i in range(NUM_RUNS):
				print TAU.format(CMD.format(FILE, n, NUM_EVENTS))
				#TODO move files
				mkdir 
				trial_count += 1


		print("\n\n")

run_trial(EXP_LIST[0])
run_trial(EXP_LIST[1])

