'''Gross script to plot statistics from nsight profiler'''

import re
import numpy as np 
import matplotlib.pyplot as plt
import sys

def reformat(array):
    Nrow=len(array)
    Ncol=len(re.split(r"\s{2,}", array[0]))
    formatted_array=np.zeros((Nrow,Ncol),dtype='object')

    for i in range(Nrow):
        formatted_array[i,:]=re.split(r"\s{2,}",array[i])
    return formatted_array


if (len(sys.argv)!=3):
    print("Usage: plot_stats_from_nsight.py profile_filename executable_filename") 
    sys.exit()

filename=sys.argv[1]
ex=sys.argv[2]


stopstart=np.zeros(8,dtype='int')
counter=0
ssindex=0
lineno=-1
with open(filename) as file:
    for line in file:
        line=line.strip()
        lineno=lineno+1
        if counter==0 and len(line)>0:
            if(line[0].isdigit()==True):
                stopstart[ssindex]=lineno
                ssindex=ssindex+1
                counter = 1
        elif counter==1 and len(line)>0:
            if(line[0].isdigit()==False):
                stopstart[ssindex]=lineno
                ssindex=ssindex+1
                counter=0

if stopstart[7]==0:
    stopstart[7]=lineno

API_stats=np.genfromtxt(filename,dtype='str',skip_header=stopstart[0],skip_footer=lineno-stopstart[1]+1)

#The rest are not working because the names have spaces in and confuse the number of columns!

kernal_stats=np.genfromtxt(filename,dtype='str',skip_header=stopstart[2],skip_footer=lineno-stopstart[3]+1,delimiter="\t")
kernal_stats=reformat(kernal_stats)

time_stats=np.genfromtxt(filename,dtype='str',skip_header=stopstart[4],skip_footer=lineno-stopstart[5]+1,delimiter=r'/n')
time_stats=reformat(time_stats)

mem_stats=np.genfromtxt(filename,dtype='str',skip_header=stopstart[6],skip_footer=lineno-stopstart[7]+1,delimiter=r'/n')
mem_stats=reformat(mem_stats)

#next add names in list of lists and then include in genfromtxt
'''
print(API_stats[:,0])
print(API_stats[:,7])
plt.figure()
plt.title("CUDA API Statistics for shoc_standalone")
y = API_stats[:,0]
mylabels = API_stats[:,7]
plt.pie(y, labels = mylabels)
plt.savefig("APIstats.pdf")
plt.savefig("APIstats.png")
plt.show()
print("---------------------------------")

print(kernal_stats[:,0])
print(kernal_stats[:,7])
plt.figure()
plt.title("Kernal Statistics for shoc_standalone")
y = kernal_stats[:,0]
mylabels = kernal_stats[:,7]
plt.pie(y, labels = mylabels)
plt.savefig("kernalstats.pdf")
plt.savefig("kernalstats.png")
plt.show()
print("---------------------------------")


print(time_stats[:,0])
print(time_stats[:,7])
plt.figure()
plt.title("CUDA Memory Operation Statistics for shoc_standalone \n (by time)")
y = time_stats[:,0]
mylabels = time_stats[:,7]
plt.pie(y, labels = mylabels)
plt.savefig("timestats.pdf")
plt.savefig("timestats.png")
plt.show()
print("---------------------------------")

print(mem_stats[:,0])
print(mem_stats[:,6])
'''

plt.figure()
plt.title("API Statistics for " +ex+"  \n (by time)")
mylabels = API_stats[:,7]
size = [s.replace(",", "") for s in API_stats[:,1]]
size = np.array(size).astype('float')
x_pos = [i for i, _ in enumerate(mylabels)]
plt.bar(x_pos, size, color='green')
plt.ylabel("Total Time (ns)")
plt.xticks(x_pos, mylabels,rotation=90)
plt.tight_layout()
plt.yscale('log')
plt.savefig("APIstatsbar_" +ex+".pdf")
plt.savefig("APIstatsbar_" +ex+".png")
plt.show()
print("---------------------------------")


plt.figure()
plt.title("Kernal Statistics for " +ex+"\n (by time)")
mylabels = kernal_stats[:,7]
size = [s.replace(",", "") for s in kernal_stats[:,1]]
size = np.array(size).astype('float')
x_pos = [i for i, _ in enumerate(mylabels)]
plt.bar(x_pos, size, color='green')
plt.ylabel("Total Time (ns)")
plt.xticks(x_pos, mylabels,rotation=90)
plt.tight_layout()
plt.yscale('log')
plt.savefig("kernalstatsbar_" +ex+".pdf")
plt.savefig("kernalstatsbar_" +ex+".png")
plt.show()
print("---------------------------------")


plt.figure()
plt.title("CUDA Memory Operation Statistics for " +ex+"  \n (by time)")
mylabels = time_stats[:,7]
size = [s.replace(",", "") for s in time_stats[:,1]]
size = np.array(size).astype('float')
x_pos = [i for i, _ in enumerate(mylabels)]
plt.bar(x_pos, size, color='green')
plt.ylabel("Total Time (ns)")
plt.xticks(x_pos, mylabels)
plt.tight_layout()
plt.savefig("timestatsbar_" +ex+".pdf")
plt.savefig("timestatsbar_" +ex+".png")
plt.show()
print("---------------------------------")



plt.figure()
plt.title("CUDA Memory Operation Statistics for " +ex+"  \n (by size)")
mylabels = mem_stats[:,6]
size = mem_stats[:,0].astype('float')
x_pos = [i for i, _ in enumerate(mylabels)]
plt.bar(x_pos, size, color='green')
plt.ylabel("Size (KiB)")
plt.xticks(x_pos, mylabels)
plt.savefig("sizestats_" +ex+".pdf")
plt.savefig("sizestats_" +ex+".png")
plt.show()
print("---------------------------------")

