#!/bin/python

#!/bin/python

'''
This is a script to run scaling experiments on the mictest program
it puts them in the .tau/mictest_sampling/manual_scaling_TTbar35_cache' directory
or ...TTbar70_cache
'''

import os
import subprocess as sp

machine = 'Sansa'

# define where the data will go
DIR  = '.tau/mictest_sampling/'

# define which simulation file to use
FILE35 = 'TTbar35PU-memoryFile.fv3.clean.writeAll.recT.072617.bin'
FILE70 = 'TTbar70PU-memoryFile.fv3.clean.writeAll.recT.072617.bin'
FILELarge = 'memoryFile.fv3.clean.writeAll.recT.072617.bin'

SBATCH = "srun --partition=short --job-name=mkFit_{:d} --nodes=1 --ntasks-per-node=1 --cpus-per-task={:d} --time=1-00:00:00 "

NUM_RUNS = 5
NUM_EVENTS=100

FILE_DIR = '/projects/hpcl/bgravell/mictest_sampling/'
FILE35 = 'TTbar35PU-memoryFile.fv3.clean.writeAll.recT.072617.bin'
FILE70 = 'TTbar70PU-memoryFile.fv3.clean.writeAll.recT.072617.bin'
FILELarge = 'memoryFile.fv3.clean.writeAll.recT.072617.bin'


if machine == 'Grover':
	TAU_DIR = '/home/users/gravelle/taucmdr-enterprise-2/system/tau/tau-2.27'
	TAU_MAKE = 'Makefile.tau-93948b87-icpc-papi-tbb'
	TAU = 'tau_exec -T 93948b87,tbb,papi,serial,icpc -ebs {:s}'
	CMD  = './mkFit/mkFit --cmssw-n2seeds --input-file {:s} --build-ce --num-thr {:d} --num-events {:d} --silent'
	SLURM = False
	EXP_LIST = ['manual_scaling_TTbar35', 'manual_scaling_TTbar70', 'manual_scaling_Large']
	THREAD_LIST = [1, 8, 16, 32, 64, 128, 256]


if machine == 'Sansa':
	TAU_DIR = '/shared/soft/taucmdr-enterprise/system/tau/tau-2.27'
	TAU_MAKE = 'Makefile.tau-5f0b2b79-icpc-papi-tbb' 
	TAU = 'tau_exec -T 5f0b2b79,tbb,papi,serial,icpc -ebs {:s}'
	CMD  = './mkFit/mkFit --cmssw-n2seeds --input-file {:s} --build-ce --num-thr {:d} --num-events {:d} --silent'
	SLURM = False
	EXP_LIST = ['manual_scaling_TTbar35', 'manual_scaling_TTbar70', 'manual_scaling_Large']
	THREAD_LIST = [1, 8, 16, 32]

if machine == 'Talapas':
	TAU_DIR = '/projects/hpcl/shared/taucmdr-enterprise/system/tau/tau-2.27/'
	TAU_MAKE = 'Makefile.tau-05c9fa46-icpc-papi-tbb'
	CMD  = 'mkFit --cmssw-n2seeds --input-file {:s} --build-ce --num-thr {:d} --num-events {:d} --silent'
	TAU = 'tau_exec -T 05c9fa46,tbb,papi,serial,icpc -ebs {:s}'
	SLURM = True
	EXP_LIST = ['manual_scaling_TTbar35_talapas', 'manual_scaling_TTbar70_talapas', 'manual_scaling_Large_talapas', \
		'manual_scaling_TTbar35_talapas_fullnode', 'manual_scaling_TTbar70_talapas_fullnode', 'manual_scaling_Large_talapas_fullnode']
	THREAD_LIST = [1, 8, 16, 32, 48, 56]
	FILE_DIR = '/projects/hpcl/bgravell/mictest_sampling/'

ENV  = [('TAU_MAKEFILE', TAU_DIR + '/x86_64/lib/' + TAU_MAKE), \
('TAU_ROOT', TAU_DIR),\
('TAU_CALLPATH','1'),\
('TAU_CALLPATH_DEPTH','100'),\
('TAU_UNWIND','1')] 
PATH=('PATH', TAU_DIR + '/x86_64/bin')

env = dict(os.environ)
for var,val in ENV:
	env[var] =  val

env[PATH[0]] = PATH[1] + ':' + env[PATH[0]]


if machine == 'Grover':
	METRIC_LIST = ['PAPI_TLB_DM', \
	'PAPI_BR_INS', 'PAPI_BR_CN', 'PAPI_BR_UCN', 'PAPI_BR_MSP',\
	'PAPI_NATIVE_UOPS_RETIRED:SCALAR_SIMD','PAPI_NATIVE_UOPS_RETIRED:PACKED_SIMD',\
	'PAPI_TOT_CYC','PAPI_TOT_INS',\
	'PAPI_L2_TCM', 'PAPI_L2_TCA',\
	'PAPI_RES_STL',\
	'PAPI_LST_INS', 'PAPI_L1_TCM',\
	'PAPI_NATIVE_LLC_REFERENCES','PAPI_NATIVE_LLC_MISSES']



if machine == 'Talapas':
	METRIC_LIST = ['PAPI_TLB_DM', 'PAPI_TLB_IM', \
	'PAPI_BR_INS', 'PAPI_BR_CN', 'PAPI_BR_MSP',\
	'PAPI_SP_OPS', 'PAPI_DP_OPS', 'PAPI_VEC_SP', 'PAPI_VEC_DP', \
	'PAPI_TOT_CYC','PAPI_TOT_INS', 'PAPI_RES_STL',\
	'PAPI_L1_TCM', 'PAPI_LST_INS' \
	'PAPI_L2_TCM', 'PAPI_L2_TCA',\
	'PAPI_L3_TCM', 'PAPI_L3_TCA']


if machine == 'Sansa':
	METRIC_LIST = ['PAPI_TLB_DM', \
	'PAPI_BR_INS', 'PAPI_BR_CN', 'PAPI_BR_UCN', 'PAPI_BR_MSP',\
	'PAPI_TOT_CYC','PAPI_TOT_INS',\
	'PAPI_L1_TCM', 'PAPI_L1_TCA',\
	'PAPI_L2_TCM', 'PAPI_L2_TCA',\
	'PAPI_L3_TCM', 'PAPI_L3_TCA',\
	'PAPI_RES_STL',\
	'PAPI_LST_INS',\
	'PAPI_FP_OPS','PAPI_SP_OPS','PAPI_DP_OPS',\
	'PAPI_VEC_SP','PAPI_VEC_DP']


def run_trial(exp_name, in_file, slurm=True, full_node=False):
	'''
	exp_name is the name of the mimiced taucmdr experiment
	it will be used as the subdirectory under DIR
	it will be sompletely overwritten so don't leave important things there
	'''

	#os.removedirs(DIR + exp_name)
	sp.Popen('rm -rf ' + DIR + exp_name, shell=True, env=env).wait()
	sp.Popen('mkdir ' + DIR + exp_name, shell=True, env=env).wait()

	trial_count = 0

	ntrials = len(METRIC_LIST) * len(THREAD_LIST) * NUM_RUNS
	sub_procs = [None for x in range(ntrials)]

	for m in METRIC_LIST:
		env['TAU_METRICS'] =  'TIME,' + m

		for n in THREAD_LIST:
				
			if full_node:
				ncores=28
			else:
				ncores=n/2+n%2

			for i in range(NUM_RUNS):
				
				# build the commands to start trials
				# make a new directory for results, go there, run new process
				trial_dir =  DIR + exp_name + '/' + str(trial_count)
				if slurm:
					trial_cmd = SBATCH.format(n,ncores) + TAU.format(CMD.format(in_file, n, NUM_EVENTS))
				else:
					trial_cmd = TAU.format(CMD.format(in_file, n, NUM_EVENTS))
				# its a little hacky but it'll have to do
				if machine == 'Talapas':
					cmd_li = ['mkdir ' + trial_dir, 'cd ' + trial_dir, 'cp /projects/hpcl/bgravell/mictest_sampling/Geoms/CMS-2017.so .', trial_cmd, 'rm CMS-2017.so']
				else:
					cmd_li = ['mkdir ' + trial_dir, trial_cmd, 'mv MULTI__* ' + trial_dir]

				cmd = build_cmd(cmd_li)

				
				if(slurm):
					print cmd
					sub_procs[trial_count] = sp.Popen(cmd, shell=True, env=env)
				else:
					# print(cmd)
					sub_procs[trial_count] = sp.Popen(cmd, shell=True, env=env).wait()

				trial_count += 1

		print("\n\n")


	for proc in sub_procs:
		proc.wait()


def build_cmd(cmd_li):
	s = cmd_li[0]
	for c in range(len(cmd_li)-1):
		s = s + '; ' + cmd_li[c+1]

	return s


if machine == 'Talapas':
	run_trial(EXP_LIST[0],FILE_DIR+FILE35,SLURM)
	run_trial(EXP_LIST[1],FILE_DIR+FILE70,SLURM)
	NUM_EVENTS=4550
	run_trial(EXP_LIST[2],FILE_DIR+FILELarge,SLURM)
	NUM_EVENTS=100
	run_trial(EXP_LIST[3],FILE_DIR+FILE35,SLURM,True)
	run_trial(EXP_LIST[4],FILE_DIR+FILE70,SLURM,True)
	NUM_EVENTS=4550
	run_trial(EXP_LIST[5],FILE_DIR+FILELarge,SLURM,True)
else:
	run_trial(EXP_LIST[0],FILE35,SLURM)
	run_trial(EXP_LIST[1],FILE70,SLURM)
	NUM_EVENTS=4550
	run_trial(EXP_LIST[2],FILELarge,SLURM)

#run_trial('test',FILE_DIR+FILE35,SLURM)
#run_trial('test',FILE_DIR+FILE35,SLURM)


def test():
	sp.Popen('rm -rf .tau/mictest_sampling/test/; mkdir .tau/mictest_sampling/test/', shell=True, env=env).wait()
	env['TAU_METRICS'] =  'TIME,PAPI_TOT_INS'
	cmd_li = ['mkdir .tau/mictest_sampling/test/0',\
			 'cd .tau/mictest_sampling/test/0',\
			 SBATCH.format(4,2) + TAU.format(CMD.format(FILE_DIR+FILE35, 4, NUM_EVENTS))]
	cmd = build_cmd(cmd_li)
	print cmd
	p=sp.Popen(cmd, shell=True, env=env)
	p.wait()

#test()


