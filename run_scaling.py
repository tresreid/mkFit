#!/bin/python

#!/bin/python

'''
This is a script to run scaling experiments on the mictest program
it puts them in the .tau/mictest_sampling/manual_scaling_TTbar35_cache' directory
or ...TTbar70_cache
'''

import os
import subprocess as sp

machine = 'Cori'

# define where the data will go
DIR  = '.tau/mictest_sampling/'

# define which simulation file to use
FILE35 = 'TTbar35PU-memoryFile.fv3.clean.writeAll.recT.072617.bin'
FILE70 = 'TTbar70PU-memoryFile.fv3.clean.writeAll.recT.072617.bin'
FILELarge = 'memoryFile.fv3.clean.writeAll.recT.072617.bin'


NUM_RUNS = 1
NUM_EVENTS=100

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
	PART = "short"
	SBATCH = "srun --partition={:s} --job-name=mkFit_{:d} --nodes=1 --ntasks-per-node=1 --cpus-per-task={:d} --time=1-00:00:00 "


if machine == 'Cori':
	TAU_DIR = '/global/homes/g/gravelle/tau2'
	TAU_MAKE = 'Makefile.tau-icpc-papi-tbb'
	TAU = 'tau_exec -T tbb,papi,serial,icpc -ebs {:s}'
	# CMD  = 'mkFit --cmssw-n2seeds --input-file {:s} --build-ce --num-thr {:d} --num-events {:d} --silent'
	CMD  = 'python run_cori.py {:d} {:d} {:s} {:s} {:s}' # num threads num events exp name file name dir
	SLURM = True
	EXP_LIST = ['manual_scaling_TTbar35', 'manual_scaling_TTbar70', 'manual_scaling_Large',\
	            'mixed_thr_scaling_TTbar35', 'mixed_thr_scaling_TTbar70', 'mixed_thr_scaling_Large']
	# THREAD_LIST = [1, 8, 16, 32, 64, 128, 256]
	# THREAD_LIST = [48, 80, 96, 112, 144, 160, 176, 192, 208, 224, 240]
	THREAD_LIST = [4, 8, 16, 32, 48, 64, 80, 96]
	# THREAD_LIST = [4, 8, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 256]
	PART = "regular"
	SBATCH = "srun --qos={:s} --job-name=mkFit_{:d} --nodes=1 --ntasks-per-node=1 --cpus-per-task={:d} --time=2-00:00:00 --constraint=knl  "
	FILE_DIR = '/project/projectdirs/m2956/gravelle/mictest_sampling/'
	NUM_RUNS = 3
	DIR  = '.tau/cori_scaling/'
	RUN_CNT = 5


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

if SLURM: 
	PATH=('PATH', FILE_DIR+'mkFit/')
	env[PATH[0]] = PATH[1] + ':' + env[PATH[0]]
	LD_PATH = ('LD_LIBRARY_PATH', FILE_DIR, FILE_DIR+'Geoms/', '.')
	env[LD_PATH[0]] = LD_PATH[1] + ':' + LD_PATH[2] + ':' + LD_PATH[3] + ':' + env[LD_PATH[0]] 


if machine == 'Grover' or machine == 'Cori':
	METRIC_LIST = ['PAPI_TLB_DM', \
	'PAPI_BR_INS', 'PAPI_BR_CN', 'PAPI_BR_UCN', 'PAPI_BR_MSP',\
	'PAPI_NATIVE_UOPS_RETIRED:SCALAR_SIMD','PAPI_NATIVE_UOPS_RETIRED:PACKED_SIMD',\
	'PAPI_TOT_CYC','PAPI_TOT_INS',\
	'PAPI_L2_TCM', 'PAPI_L2_TCA',\
	'PAPI_RES_STL',\
	'PAPI_LST_INS', 'PAPI_L1_TCM',\
	'PAPI_NATIVE_LLC_REFERENCES','PAPI_NATIVE_LLC_MISSES',\
	'PAPI_NATIVE_FETCH_STALL', 'PAPI_NATIVE_RS_FULL_STALL']

	# METRIC_LIST = ['PAPI_NATIVE_FETCH_STALL', 'PAPI_NATIVE_RS_FULL_STALL']
	


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

	if machine != 'Cori':
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
				if machine == 'Cori':
					trial_dir =  DIR + exp_name + '/' + str(RUN_CNT) + '_' + str(trial_count)
				else:
					trial_dir =  DIR + exp_name + '/' + str(trial_count)
				if slurm:
					trial_cmd = SBATCH.format(PART,n,ncores) + TAU.format(CMD.format(in_file, n, NUM_EVENTS))
				else:
					trial_cmd = TAU.format(CMD.format(in_file, n, NUM_EVENTS))
				# its a little hacky but it'll have to do
				if machine == 'Talapas' or machine == 'Cori':
					cmd_li = ['mkdir ' + trial_dir, 'cd ' + trial_dir, 'cp ' + FILE_DIR + 'Geoms/CMS-2017.so .', trial_cmd]
				else:
					cmd_li = ['mkdir ' + trial_dir, trial_cmd, 'mv MULTI__* ' + trial_dir]

				cmd = build_cmd(cmd_li)

				
				if(slurm):
					# print cmd
					sub_procs[trial_count] = sp.Popen(cmd, shell=True, env=env)
				else:
					# print(cmd)
					sub_procs[trial_count] = sp.Popen(cmd, shell=True, env=env).wait()

				trial_count += 1

		print("\n\n")


	for proc in sub_procs:
		if proc is not None:
			proc.wait()


def run_cori_trial(exp_name, in_file):

	sub_procs = [None for x in range(len(THREAD_LIST))]
	x = 0
	for n in THREAD_LIST:
		ncores=n/2+n%2 
		cmd = SBATCH.format(PART,n,ncores) + CMD.format(n, NUM_EVENTS, exp_name, in_file, FILE_DIR)
		
		# print cmd
		sub_procs[x] = sp.Popen(cmd, shell=True, env=env)
		x += 1

	for proc in sub_procs:
		if proc is not None:
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
elif machine == 'Cori':
	# run_cori_trial(EXP_LIST[0],FILE_DIR+FILE35)
	# run_cori_trial(EXP_LIST[1],FILE_DIR+FILE70)
	NUM_EVENTS=4550
	run_cori_trial(EXP_LIST[2],FILE_DIR+FILELarge)
else:
	run_trial(EXP_LIST[0],FILE35,SLURM)
	run_trial(EXP_LIST[1],FILE70,SLURM)
	NUM_EVENTS=4550
	run_trial(EXP_LIST[2],FILELarge,SLURM)

#run_trial('test',FILE_DIR+FILE35,SLURM)
#run_trial('test',FILE_DIR+FILE35,SLURM)


def test():
	sp.Popen('rm -rf .tau/cori_scaling/test/; mkdir .tau/cori_scaling/test/', shell=True, env=env).wait()
	#env['TAU_METRICS'] =  'TIME,PAPI_TOT_INS'
	cmd_li = ['mkdir .tau/cori_scaling/test/0',\
			 'cd .tau/cori_scaling/test/0',\
			 SBATCH.format(PART,4,2) + TAU.format(CMD.format(FILE_DIR+FILE35, 4, NUM_EVENTS))]
	cmd = build_cmd(cmd_li)
	print cmd
	p=sp.Popen(cmd, shell=True, env=env)
	#p.wait()

# test()


