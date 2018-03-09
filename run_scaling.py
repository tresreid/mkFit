#!/bin/python

'''
This is some trash to run scaling experiments on the mictest program
it puts them in the .tau/mictest_sampling/manual_scaling_TTbar35_cache' directory
or ...TTbar70_cache
'''

import os
import subprocess as sp

# Grover
'''
TAU_DIR = '/home/users/gravelle/taucmdr-enterprise-2/system/tau/tau-2.27'
ENV  = [('TAU_MAKEFILE', TAU_DIR + '/x86_64/lib/Makefile.tau-93948b87-icpc-papi-tbb'), \
('TAU_ROOT', TAU_DIR)] 
PATH=('PATH', TAU_DIR + '/x86_64/bin')
'''

# Talapas
TAU_DIR = '/projects/hpcl/shared/taucmdr-enterprise/system/tau/tau-2.27/'

ENV  = [('TAU_MAKEFILE', TAU_DIR + '/x86_64/lib/ Makefile.tau-05c9fa46-icpc-papi-tbb'), \
('TAU_ROOT', TAU_DIR),\
('TAU_CALLPATH','1'),\
('TAU_CALLPATH_DEPTH','100'),\
('TAU_UNWIND','1')] 

PATH=('PATH', TAU_DIR + '/x86_64/bin')


# define where the data will go
DIR  = '.tau/mictest_sampling/'

# define which simulation file to use
FILE = 'TTbar35PU-memoryFile.fv3.clean.writeAll.recT.072617.bin'

# mkFit command formating
CMD  = './mkFit/mkFit --cmssw-n2seeds --input-file {:s} --build-ce --num-thr {:d} --num-events {:d} --silent'

# Tau command formatting
# Grover
# TAU = 'tau_exec -T 93948b87,tbb,papi,serial,icpc -ebs {:s}'
# Talapas
TAU = 'tau_exec -T 05c9fa46,tbb,papi,serial,icpc -ebs {:s}'


SBATCH = "srun --partition=short --job-name=mkFit_{:d} --nodes=1 --ntasks-per-node=1 --time=1-00:00:00 "

NUM_RUNS = 5 
THREAD_LIST = [2, 4, 8, 16, 32, 48, 64, 96, 112, 128, 256]
NUM_EVENTS=100

env = dict(os.environ)
for var,val in ENV:
	env[var] =  val

env[PATH[0]] = PATH[1] + ':' + env[PATH[0]]

EXP_LIST = ['manual_scaling_TTbar35_cache', 'manual_scaling_TTbar70_cache']

# GROVER
'''
METRIC_LIST = ['PAPI_TLB_DM', \
'PAPI_BR_INS', 'PAPI_BR_CN', 'PAPI_BR_UCN', 'PAPI_BR_MSP',\
'PAPI_NATIVE_UOPS_RETIRED:SCALAR_SIMD','PAPI_NATIVE_UOPS_RETIRED:PACKED_SIMD',\
'PAPI_TOT_CYC','PAPI_TOT_INS',\
'PAPI_L2_TCM', 'PAPI_L2_TCA',\
'PAPI_RES_STL',\
'PAPI_LST_INS', 'PAPI_L1_TCM',\
'PAPI_NATIVE_LLC_REFERENCES','PAPI_NATIVE_LLC_MISSES']
'''

# Talapas
METRIC_LIST = ['PAPI_TLB_DM', 'PAPI_TLB_IM', \
'PAPI_BR_INS', 'PAPI_BR_CN', 'PAPI_BR_MSP',\
'PAPI_SP_OPS', 'PAPI_DP_OPS', 'PAPI_VEC_SP', 'PAPI_VEC_DP', \
'PAPI_TOT_CYC','PAPI_TOT_INS', 'PAPI_RES_STL',\
'PAPI_L1_TCM', 'PAPI_L1_TCA',\
'PAPI_L2_TCM', 'PAPI_L2_TCA',\
'PAPI_L3_TCM', 'PAPI_L3_TCA',\
'PAPI_LST_INS']


def run_trial(exp_name, slurm=False):
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
				if(slurm):
					sp.Popen(SBATCH.format(n) + TAU.format(CMD.format(FILE, n, NUM_EVENTS)), shell=True, env=env).wait()
				else:
					sp.Popen(TAU.format(CMD.format(FILE, n, NUM_EVENTS)), shell=True, env=env).wait()
				trial_dir =  DIR + exp_name + '/' + str(trial_count)
				sp.Popen('mkdir ' + trial_dir, shell=True, env=env).wait()
				sp.Popen('mv MULTI__TIME ' + trial_dir + '/MULTI__TIME', shell=True, env=env).wait()
                                sp.Popen('mv MULTI__' + m.replace(':', '_') + ' ' + trial_dir + '/MULTI__' + m.replace(':', '_'), shell=True, env=env).wait()
				trial_count += 1


		print("\n\n")

#run_trial(EXP_LIST[0])
#run_trial(EXP_LIST[1])
#run_trial('test')
env['TAU_METRICS'] =  'TIME,PAPI_TOT_INS'
print SBATCH.format(100) + TAU.format(CMD.format(FILE, 100, NUM_EVENTS))
sp.Popen(SBATCH.format(100) + TAU.format(CMD.format(FILE, 100, NUM_EVENTS)), shell=True, env=env)

