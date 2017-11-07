import os
import sys
from multiprocessing import Process
import csv

path="/home/srinivasa/sim/mafia-master/pthread_benchmark/aging_results/"
stats=['gpu_tot_sim_cycle','gpu_tot_sim_insn','total_cycles, active_cycles, idle cycles','warps_exctd_sm']

dirs=['aging_1_fcfs','aging_1_profiling','aging_1_ilp','aging_1_ilpSMRA']


f_list=[[],[],[],[]]

T_cycles_list=[[],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[]]

I_cycles_list=[[],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[]]

w_list=[[],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[],
			 [],[],[],[],[],[],[],[],[],[]]

check_list=[]

p=[None]*len(dirs)
args=[]
fp=[None]*len(dirs)


e_list=[]
def info(title):
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):  # only available on Unix
        print 'parent process:', os.getppid()
    print 'process id:', os.getpid()

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

def search_in_file(fp,op,k):
	j=0
	for i in range(len(stats)):
		while True:
			line=fp.readline()
			if not line:
				break	
			
			if stats[i] in line:
				if i == 3:
					match=line.split('=')
					if op == 'append':
						w_list[j].append(float(match[1]))
					elif op == 'add':
						#print w_list[j]
						w_list[j][k]=float(w_list[j][k])+float(match[1])
					j=j+1
					#print j
					if j==60:
						#i=i+2
						j=0
						break

				elif i == 2:
					match=line.split('=')
					match=match[1].split(',')
					if op == 'append':
						T_cycles_list[j].append(float(match[0]))
						I_cycles_list[j].append(float(match[2]))
					elif op == 'add':
						#print T_cycles_list[j]
						T_cycles_list[j][k]=float(T_cycles_list[j][k])+float(match[0])
						I_cycles_list[j][k]=float(I_cycles_list[j][k])+float(match[2])
					j=j+1
					#print j
					if j==60:
						#i=i+1
						j=0
						break
					

				else:
					match=line.split()
					#print match
					if op == 'append':
						f_list[i].append(float(match[2]))
					elif op == 'add':
						f_list[i][k]=float(f_list[i][k])+float(match[2])
					break
					




def write_csv(filenw):
    fpw=open('%s.csv' %filenw,'w')
    wr=csv.writer(fpw, quoting=csv.QUOTE_ALL)
   
    #f_list.insert(0,'Throughput')
    for i in range(len(I_cycles_list)):
	#print I_cycles_list[i]
    	wr.writerow(I_cycles_list[i])

    wr.writerow(e_list)
    for i in range(len(T_cycles_list)):
    	wr.writerow(T_cycles_list[i])
    wr.writerow(e_list)

    for i in range(len(f_list)):
	#print T_cycles_list[i]
    	wr.writerow(f_list[i])
    wr.writerow(e_list)

    for i in range(len(w_list)):
	#print w_list[i]
    	wr.writerow(w_list[i])

    fpw.close()
  

file_out='aging_test'

for i in range(len(dirs)):
	temp=path+dirs[i]
	op='append'
	for filename in os.listdir(temp):
		fp = open(temp+'/'+filename,'r')
		fp = last_kernel_launch(fp)
		search_in_file(fp,op,i)
		op='add'
		#print T_cycles_list

		fp.close()
write_csv(file_out)



'''def get_job(i):
	global path
	path=path+dirs[i]
	for filename in os.listdir(path):
		filename=path+'/'+filename
		print filename
		fp[i]=open(filename,'r')
		fp[i]=last_kernel_launch(fp[i])
		search_in_file(fp[i],i)'''



'''if __name__ == '__main__':
	info('main line')

   	for i in xrange():
		p[i] = Process(target=get_job, args=(i,))
		p[i].start()
	    
   	for i in range(dirs):
		p[i].join()
'''
