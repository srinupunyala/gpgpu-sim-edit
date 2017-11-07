from collections import Counter
import numpy
import sys

stats=['gpu_tot_sim_cycle ','gpu_tot_sim_insn','gpu_tot_ipc ',
	'gpgpu_n_load_insn','gpgpu_n_store_insn','total reads:','n_cmd','Avg_MPKI_Stream', 'L2_total_cache_accesses ' ,
	'L2_total_cache_misses ','L2_total_cache_miss_rate']

pstats=['total sim cycles','total sim instructions','total GPU ipc','total load instructions',
	'total store instructions','total MEM accesses','Mem BW utilization', 
	'Avg L2 MPKI','total L2 accesses','total L2 misses',
	'L2 miss rate']

m_stats_1=['gpu_ipc_1','gpu_tot_sim_cycle_stream_1','gpu_sim_insn_1 ', 
'n_cmd','Stream 1: Accesses ','Stream 1: Misses ','Avg_MPKI_Stream1']

m_stats_2=['gpu_ipc_2','gpu_tot_sim_cycle_stream_2','gpu_sim_insn_2 ', 
'n_cmd','Stream 2: Accesses ','Stream 2: Misses ','Avg_MPKI_Stream2']

m_p_stats=['gpu sim ipc','total sim cycles','total sim insn','Mem BW Utilization','total L2 accesses'
,'total L2 misses','total L2 Avg MPKI']

def openfile(filename,accesses):
	fp=open(filename,accesses)
	return fp

def last_kernel_launch(fp):
	kernelcount=0
 	while True:
		line=fp.readline()
		if not line:
			break
		if 'kernel_name' in line:
			kernelcount+=1
		newcount=0
	fp.seek(0,0)
	while True:
		line=fp.readline()
		if not line:
			break
		if 'kernel_name' in line:
			newcount+=1
			if newcount==kernelcount:
				break
	return fp

def search_in_file(stat,fp):
	while True:
		line=fp.readline()
		if stat in line:
			if 'icnt_total_pkts' in stat or 'Avg_MPKI_Stream' in stat:
				match=line.split('=')
				towrite=match[1]
			elif 'n_cmd' in stat:
				match=line.split()
				match=match[10].split('=')
				towrite=match[1]
			else:	
				match=line.split()
				towrite=match[2]
			return float(towrite)
		if not line:break
	
def searchset(fp,fp_w):
	for i in range(len(stats)):
		match=search_in_file(stats[i],fp)
		if i==6:
			for k in range(5):
				match+=search_in_file(stats[i],fp)
			match=match/6
		if i==5:
			match+=search_in_file(stats[i],fp)
		fp_w.write('%s = %s\n' %(pstats[i],match))

def kernels(fp):
	kernelc=[]
	while True:
		line=fp.readline()
		if 'transfer to GPU' in line:
			match=line.split()
			match=match[1].split("'")
			if match[1] not in kernelc:
				kernelc.append(match[1])		
		if not line:break
		fp.seek(0,0)
		return kernelc

def search_m_files(stat,fp):
	fp.seek(0,0)
	while True:
		line=fp.readline()
		if stat in line:
			match=line.split()
			towrite=0
			if 'n_cmd' in line:
				towrite=[]
				towrite.append(float(match[11].split('=')[1]))
				towrite.append(float(match[12].split('=')[1]))
			elif 'Stream' in line and ':' in line:
				towrite=match[4]
			elif 'Avg_MPKI' in line:
				towrite=float(match[1])
			else:
				towrite=float(match[2])
			print towrite	
			return towrite
		if not line:break

def search_m_apps(fp,fp_w,stream):
	for i in range(len(stream)):
		if i==3:
			match=[]
			match=search_m_files(stream[i],fp)
			fp_w.write('%s=%s\n' %(m_p_stats[i],match[0]))
			fp_w.write('%s=%s\n' %(m_p_stats[i],match[1]))
		else:
			match=search_m_files(stream[i],fp)
			fp_w.write('%s=%s\n' %(m_p_stats[i],match))

def f_out_stream(filename):
	test=filename.split('_')
	if test[0]==test[2]:
		return 'stream1'
	elif test[0]==test[3].split('.')[0]:
		return 'stream2'
	else:
		return 'Null'

fp=openfile(sys.argv[2],'r')

if sys.argv[1]=='-apps':
	temp=sys.argv[2].split('_')
	temp1=temp[3].split('.')
	out_file='filtered_'+temp[0]+'_with_'+temp[2]+'_'+temp1[0]+'.txt'
	fp_w=openfile(out_file,'w')
	f_stream=f_out_stream(sys.argv[2])
	if f_stream=='stream1':
		search_m_apps(fp,fp_w,m_stats_1)
	elif f_stream=='stream2':
		search_m_apps(fp,fp_w,m_stats_2)
	elif f_stream=='Null':
		print 'stream detection failed'
	
elif sys.argv[1]=='-sing0' or sys.argv[1]=='-sing':
	temp=sys.argv[2].split('_')
	temp=temp[2].split('.')
	out_file='filtered_'+temp[0]+'.txt'
	fp=last_kernel_launch(fp)

	fp_w=openfile(out_file,'w')
	searchset(fp,fp_w)
	fp_w.close()

print 'done'
fp.close()

