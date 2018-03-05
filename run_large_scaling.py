#!/bin/python

'''
This is some trash to run scaling experiments on the mictest program
it puts them in the .tau/mictest_sampling/manual_scaling_TTbar35_cache' directory
or ...TTbar70_cache
'''

import os
import subprocess as sp

TAU_DIR = '/home/users/gravelle/taucmdr-enterprise-2/system/tau/tau-2.27'
ENV  = [('TAU_MAKEFILE', TAU_DIR + '/x86_64/lib/Makefile.tau-93948b87-icpc-papi-tbb'), \
('TAU_ROOT', TAU_DIR)] 
PATH=('PATH', TAU_DIR + '/x86_64/bin')


DIR  = '.tau/mictest_sampling/'
#FILE = 'TTbar35PU-memoryFile.fv3.clean.writeAll.recT.072617.bin'
FILE = 'memoryFile.fv3.clean.writeAll.recT.072617.bin'
CMD  = './mkFit/mkFit --cmssw-n2seeds --input-file {:s} --build-ce --num-thr {:d} --num-events {:d} --silent'

TAU = 'tau_exec -T 93948b87,tbb,papi,serial,icpc -ebs {:s}'

NUM_RUNS = 3
THREAD_LIST = [2, 8, 16, 32, 64, 128, 192, 256]
#THREAD_LIST = [2, 4, 8]
NUM_EVENTS=4550

env = dict(os.environ)
for var,val in ENV:
	env[var] =  val

env[PATH[0]] = PATH[1] + ':' + env[PATH[0]]

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

	#os.removedirs(DIR + exp_name)
	sp.Popen('rm -rf ' + DIR + exp_name, shell=True, env=env).wait()
	sp.Popen('mkdir ' + DIR + exp_name, shell=True, env=env).wait()

	trial_count = 0

	for m in METRIC_LIST:
		env['TAU_METRICS'] =  'TIME,' + m

		for n in THREAD_LIST:
			for i in range(NUM_RUNS):
				sp.Popen(TAU.format(CMD.format(FILE, n, NUM_EVENTS)), shell=True, env=env).wait()
				trial_dir =  DIR + exp_name + '/' + str(trial_count)
				sp.Popen('mkdir ' + trial_dir, shell=True, env=env).wait()
				sp.Popen('mv MULTI__TIME ' + trial_dir + '/MULTI__TIME', shell=True, env=env).wait()
                                sp.Popen('mv MULTI__' + m.replace(':', '_') + ' ' + trial_dir + '/MULTI__' + m.replace(':', '_'), shell=True, env=env).wait()
				trial_count += 1


		print("\n\n")

#run_trial(EXP_LIST[0])
#run_trial(EXP_LIST[1])
run_trial('manual_scaling_large_cache')

#print TAU.format(CMD.format(FILE, 256, NUM_EVENTS))
#sp.Popen(TAU.format(CMD.format(FILE, 256, NUM_EVENTS)), shell=True, env=env).wait()

