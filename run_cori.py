#!/bin/python


'''
This is a script to run scaling experiments on the mictest program
it puts them in the .tau/mictest_sampling/manual_scaling_TTbar35_cache' directory
or ...TTbar70_cache
'''

import os
import subprocess as sp
import sys


num_thread = int(sys.argv[1])
NUM_EVENTS = int(sys.argv[2])
EXP_NAME   = sys.argv[3]
FILE_NAME   = sys.argv[4]
FILE_DIR   = sys.argv[5]

machine = 'Cori'

# define where the data will go
DIR  = '.tau/mictest_sampling/'

TAU_DIR = '/global/homes/g/gravelle/tau2'
TAU_MAKE = 'Makefile.tau-icpc-papi-tbb'
TAU = 'tau_exec -T tbb,papi,serial,icpc -ebs {:s}'
CMD  = 'mkFit --cmssw-n2seeds --input-file {0:s} --build-ce --num-thr {1:d} --num-thr-ev {2:d} --num-events {3:d} --silent'
SLURM = True
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
	
# this is probably what to change to do rooflines on cori
# make the cmd run the benchmark and adjust the METRIC file appropriately
def run_trial(exp_name, in_file, slurm=True, full_node=False, ev_thread=False):
	'''
	exp_name is the name of the mimiced taucmdr experiment
	it will be used as the subdirectory under DIR
	it will be sompletely overwritten so don't leave important things there
	'''

	trial_count = 0
	if ev_thread: num_ev_thread = int(num_thread/4)
	else: num_ev_thread = 1
	trial_cmd = TAU.format(CMD.format(in_file, num_thread, num_ev_thread, NUM_EVENTS))

	for m in METRIC_LIST:
		env['TAU_METRICS'] =  'TIME,' + m

		for i in range(NUM_RUNS):
			
			# build the commands to start trials
			# make a new directory for results, go there, run new process
			trial_dir =  DIR + exp_name + '/' + str(RUN_CNT) + '_' + str(num_thread) + '_' + str(trial_count)
			# its a little hacky but it'll have to do
			cmd_li = ['mkdir ' + trial_dir, 'cd ' + trial_dir, 'cp ' + FILE_DIR + 'Geoms/CMS-2017.so .', trial_cmd, 'cd '+FILE_DIR]
			
			cmd = build_cmd(cmd_li)

			# print cmd
			proc = sp.Popen(cmd, shell=True, env=env).wait()

			trial_count += 1 


def build_cmd(cmd_li):
	s = cmd_li[0]
	for c in range(len(cmd_li)-1):
		s = s + '; ' + cmd_li[c+1]

	return s


if machine == 'Cori':
	# run_trial(EXP_LIST[0],FILE_DIR+FILE35,SLURM)
	run_trial(EXP_NAME, FILE_NAME, SLURM, ev_thread=False)
	# NUM_EVENTS=4550
	# run_trial(EXP_LIST[2],FILE_DIR+FILELarge,SLURM)



