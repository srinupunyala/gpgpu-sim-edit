import csv
import numpy as np
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

apps=['BFS2','BLK', 'BP', 'LUD' ,'FFT', 'JPEG', '3DS', 'HS', 'LPS', 'RAY', 'GUPS', 'SPMV', 'SAD', 'NN']

papps=['','BFS2','','','','','','BLK','','','','','','BP','','','','', '','LUD' ,'','','','','','FFT','','','','','','JPEG','',
'','','','','3DS','','','','','','HS','','','','','','LPS','','','','', '','RAY','','',
'','', '','GUPS','','','','','','SPMV','','','','','', 'SAD','','','','','','NN']

pstats=['Total cycles','Total instructions','ipc','load insn',
	'store insn','MEM accesses','MemBW utlization', 
	'Avg L2 MPKI','L2 accesses','L2 misses','L2 miss rate']
	
stat=['cycles','insn','ipc','loadinsn','storeinsn','memaccesses', 
'MemoryBW','l2mpki','l2accesses','l2misses','l2missrate']

#configs=['10','15','20','30','2C','1/2 c','no l1']
configs=['l1','no l1']
pconfigs=['cores','10','15','20','30','2C','1/2 c','10','15','20','30','2C','1/2 c','10','15','20','30','2C','1/2 c',
			'10','15','20','30','2C','1/2 c','10','15','20','30','2C','1/2 c','10','15','20','30','2C','1/2 c','10',
			'15','20','30','2C','1/2 c','10','15','20','30','2C','1/2 c','10','15','20','30','2C','1/2 c','10','15',
			'20','30','2C','1/2 c','10','15','20','30','2C','1/2 c','10','15','20','30','2C','1/2 c','10','15','20',
			'30','2C','1/2 c','10','15','20','30','2C','1/2 c']

#dirs=['1_sing_10','1_sing_15','1_sing_20','1_sing_30','1_sing_2c','1_sing_hc','2_sing_L1_Off']
dirs=['1_sing_30','2_sing_60']
m_p_stats=['gpu sim ipc','total sim cycles','total sim insn','Mem BW Utilization','total L2 accesses'
,'total L2 misses','total L2 Avg MPKI']

#full_list=[ [ [],[],[],[],[],[],[],[],[],[],[] ],
#	        [ [],[],[],[],[],[],[],[],[],[],[] ],
#	    	[ [],[],[],[],[],[],[],[],[],[],[] ],
#	    	[ [],[],[],[],[],[],[],[],[],[],[] ],
#	    	[ [],[],[],[],[],[],[],[],[],[],[] ],
#	    	[ [],[],[],[],[],[],[],[],[],[],[] ],
#		[ [],[],[],[],[],[],[],[],[],[],[] ] ]

#norm_list=[ [ [],[],[],[],[],[],[],[],[],[],[] ],
#	  	  	[ [],[],[],[],[],[],[],[],[],[],[] ],
#	 	    [ [],[],[],[],[],[],[],[],[],[],[] ],
#	 	    [ [],[],[],[],[],[],[],[],[],[],[] ],
#	 	    [ [],[],[],[],[],[],[],[],[],[],[] ],
	#	    [ [],[],[],[],[],[],[],[],[],[],[] ],
	 #   	[ [],[],[],[],[],[],[],[],[],[],[] ] ]

full_list=[ [ [],[],[],[],[],[],[],[],[],[],[] ],
                [ [],[],[],[],[],[],[],[],[],[],[] ] ]

norm_list=[ [ [],[],[],[],[],[],[],[],[],[],[] ],
                [ [],[],[],[],[],[],[],[],[],[],[] ] ]

write_list=[ [],[],[],[],[],[],[],[],[],[],[] ]

def search_file(conf,app):
	statnum=0
	fp=open('%s/filtered_%s.txt' %(dirs[conf],app),'r');
	while True:
		line=fp.readline()
		if '=' in line:
			match=line.split()
			full_list[conf][statnum].append(float(match[4]))
		statnum+=1
		#if statnum==10:break
		if not line:break

def gather_all():
	print '----gathering results!!----\n'
	for i in range(len(configs)):
		for j in range(len(apps)):	
			search_file(i,apps[j])
	print '\ndone !\n'
		
def normalize():
	print '----normalizing results----!'
	for i in range(len(configs)):
		for j in range(len(stat)):
			with np.errstate(divide='ignore', invalid='ignore'):
				norm_list[i][j]=np.true_divide(full_list[i][j],full_list[0][j])
				norm_list[i][j][ ~ np.isfinite( norm_list[i][j] )] = 0
	print '\ndone !\n'
			
def plot_results():
	barwidth=0.11
	opacity=0.8
	x=np.arange(len(apps))
	pdf=matplotlib.backends.backend_pdf.PdfPages("graphs_30-60_all.pdf")
	print '----plotting results!----\n'
	for j in range(len(stat)):
		ax=j%2
		if ax==0:
			fig,axes=plt.subplots(nrows=2,ncols=1)		
		plt.setp(axes,xticks=x,xticklabels=apps)
		plt.sca(axes[ax])
		plt.bar(x, norm_list[0][j], barwidth, color='green', label='10 cores',alpha=opacity)
		plt.bar(x+barwidth, norm_list[1][j], barwidth, color='pink', label='15 cores',alpha=opacity)
		#plt.bar(x+2*barwidth, norm_list[2][j],barwidth, color='yellow', label='20 cores',alpha=opacity)
		#plt.bar(x+3*barwidth, norm_list[3][j],barwidth, color='orange', label='30 cores',alpha=opacity)
		#plt.bar(x+4*barwidth, norm_list[4][j],barwidth, color='blue', label='30 cores double cache sets',alpha=opacity)
		#plt.bar(x+5*barwidth, norm_list[5][j],barwidth, color='navy', label='30 cores half cache sets',alpha=opacity)
		#plt.bar(x+6*barwidth, norm_list[6][j],barwidth, color='red', label='30 cores l1 off',alpha=opacity)
		plt.title(pstats[j])
		if j==0: plt.legend(loc=2,prop={'size':7})

	for fig in xrange(1, figure().number):
		pdf.savefig( fig )
	pdf.close()

	print '\ndone !\n'

def mergelists(writelist):
	print '\nstatus : merging lists'
	for i in range(len(stat)):
		write_list[i]=[None]*2*len(writelist[0][0])
		for j in range(len(configs)):
			write_list[i][j::2]=writelist[j][i]

def write_csv(filenw,whichlist):
	fpw=open('%s.csv' %filenw,'w')
	wr=csv.writer(fpw, quoting=csv.QUOTE_ALL)
	mergelists(whichlist)
	wr.writerow(papps)
	wr.writerow(pconfigs)
	for i in range(len(stat)):
		write_list[i].insert(0,pstats[i])
		wr.writerow(write_list[i])
	print '\ndone !\n'
	
def kernels(fp):
	while True:
		line=fp.readline()
		if 'transfer to GPU' in line:
			match=line.split()
			match=match[1].split("'")
			if match[1] not in kernelc:
				kernelc.append(match[1])		
		if not line:break
		fp.seek(0,0)
					
gather_all()
normalize()

print '----wrting full results!----'
filenw='full_results_new'
#write_csv(filenw,full_list)

print '----wrting normalized results!----'
filenw='normalized_results_new'
#write_csv(filenw,norm_list)

plot_results()

del full_list[:]
del norm_list[:]
del write_list[:]
