#!/bin/python
import collections
import re
import sys
from collections import OrderedDict
from datetime import datetime


def convert_time(e,s):
    FMT = '%H:%M:%S'
    tdelta = datetime.strptime(e, FMT) - datetime.strptime(s, FMT)
    seconds = tdelta.total_seconds()
    return seconds   

#logfile="/usr/local/hadoop-1.2.1/logs/hadoop-cloudsys-jobtracker-161-vm1.log.2016-03-09"
#logfile="/usr/local/hadoop-1.2.1/logs/hadoop-cloudsys-jobtracker-161-vm1.log.2016-03-10"
logfile="/usr/local/hadoop-1.2.1/logs/hadoop-cloudsys-jobtracker-161-vm1.log"

a=open(logfile,"r")
d=OrderedDict()
jobfound = 0;

if len(sys.argv) < 2:
    print "provide job id";
    sys.exit();

jobid = sys.argv[1];

for line in a:
    if jobfound == 1 and "JobSummary" in line:
        break;

    if "Adding task (MAP) 'attempt_" + jobid +"_m" in line:
        jobfound = 1;
        tn=((int(line.split( )[7].split('_')[4].strip('\''))))
        st=line.split(',')[0]
        nn=line.split()[13].split(':',1)[0].split('_')[1].split('vm')[1]
        an=((int(line.split( )[7].split('_')[5].strip('\''))))
        et=0
        #tn: task number
        #an: task attempt number
        #et: task finish time
        #st: task start time
        #nn: node number
        #0: task success
        #1: task killed
        d[tn,an]=[et,st,nn,0]
        
    elif "has completed task_" + jobid + "_m" in line:
        tn=((int(line.split( )[5].split('_')[4].strip('\''))))
        an=((int(line.split( )[5].split('_')[5].strip('\''))))
        et=line.split(',')[0]
        if((tn,an) in d):
           d[tn,an][0]=et
    elif "Removing task 'attempt_" + jobid +"_m" in line:
        tn=((int(line.split( )[6].split('_')[4].strip('\''))))
        an=((int(line.split( )[6].split('_')[5].strip('\''))))
        et=line.split(',')[0]
        if((tn,an) in d) and d[tn,an][0] == 0:
           d[tn,an][0]=et
           d[tn,an][3]=1

        
ds=sorted(d.items())

dlen=len(ds)


fout2 = open("data2.txt",'w')
fout3 = open("data3.txt",'w')
fout4 = open("data4.txt",'w')
fout5 = open("data5.txt",'w')
fout6 = open("data6.txt",'w')
#fout7 = open("data7.txt",'w')
#fout8 = open("data8.txt",'w')
#fout9 = open("data9.txt",'w')
#fout10 = open("data10.txt",'w')
#fout11 = open("data11.txt",'w')

#fkill = open("fkillm_0074.txt",'w')

for i in range (0,dlen):
    e=str(ds[i][1][0])
    s=str(ds[i][1][1])
    
    print ds[i];
     
    if ds[i][1][3]==0:  
      strout="m"+str(ds[i][0][0])+"_"+str(ds[i][0][1])+" "+str(s.split( )[1])+" "+str(e.split( )[1])+"\n" 
    else:
      strout="kill_m"+str(ds[i][0][0])+"_"+str(ds[i][0][1])+" "+str(s.split( )[1])+" "+str(e.split( )[1])+"\n" 
    
    if ds[i][1][2]=="2":
      fout2.write(strout)
    elif ds[i][1][2]=="3":
      fout3.write(strout)
    elif ds[i][1][2]=="4":
      fout4.write(strout)
    elif ds[i][1][2]=="5":
      fout5.write(strout)
    elif ds[i][1][2]=="6":
      fout6.write(strout)
 #   elif ds[i][1][2]=="7" and ds[i][1][0]!=0:
 #       fout7.write(str(convert_time(e.split( )[1],s.split( )[1]))+"\n")
     
        
#fkill.close()        
#fout2.close()
#fout3.close()
#fout4.close()
#fout5.close()
#fout6.close()
#fout7.close()

print "\n----------------\n";

b=open(logfile,"r")
d=OrderedDict()
jobfound = 0;
for line in b:

    if jobfound == 1 and "JobSummary" in line:
        break;

    if "Adding task (REDUCE) 'attempt_" + jobid + "_r" in line:
        jobfound = 1;
        tn=((int(line.split( )[7].split('_')[4].strip('\''))))
        st=line.split(',')[0]
        nn=line.split()[13].split(':',1)[0].split('_')[1].split('vm')[1]
        an=((int(line.split( )[7].split('_')[5].strip('\''))))
        et=0
        
        d[tn,an]=[et,st,nn,0]
        
    elif "has completed task_" + jobid + "_r" in line:
        tn=((int(line.split( )[5].split('_')[4].strip('\''))))
        an=((int(line.split( )[5].split('_')[5].strip('\''))))
        et=line.split(',')[0]
        if((tn,an) in d):
           d[tn,an][0]=et
    
    elif "Removing task 'attempt_" + jobid +"_r" in line:
        tn=((int(line.split( )[6].split('_')[4].strip('\''))))
        an=((int(line.split( )[6].split('_')[5].strip('\''))))
        et=line.split(',')[0]
        if((tn,an) in d) and d[tn,an][0] == 0:
           d[tn,an][0]=et
           d[tn,an][3]=1

ds=sorted(d.items())

dlen=len(ds)


fout2r = open("data2r.txt",'w')
fout3r = open("data3r.txt",'w')
fout4r = open("data4r.txt",'w')
fout5r = open("data5r.txt",'w')
fout6r = open("data6r.txt",'w')
#fout7r = open("data7r.txt",'w')
#fout8r = open("data8r.txt",'w')
#fout9r = open("data9r.txt",'w')
#fout10r = open("data10r.txt",'w')
#fout11r = open("data11r.txt",'w')

#fkillr = open("fkillr_0074.txt",'w')

for i in range (0,dlen):
    e=ds[i][1][0]
    s=ds[i][1][1]
 
    print ds[i];
       
       
    if ds[i][1][3]==0:  
      strout="r"+str(ds[i][0][0])+"_"+str(ds[i][0][1])+" "+str(s.split( )[1])+" "+str(e.split( )[1])+"\n" 
    else:
      strout="kill_r"+str(ds[i][0][0])+"_"+str(ds[i][0][1])+" "+str(s.split( )[1])+" "+str(e.split( )[1])+"\n" 
    
    if ds[i][1][2]=="2":
      fout2r.write(strout)
    elif ds[i][1][2]=="3":
      fout3r.write(strout)
    elif ds[i][1][2]=="4":
      fout4r.write(strout)
    elif ds[i][1][2]=="5":
      fout5r.write(strout)
    elif ds[i][1][2]=="6":
      fout6r.write(strout)
 
        
#fout2r.close()
#fout3r.close()
#fout4r.close()
#fout5r.close()
#fout6r.close()
#fout7r.close()
#fkillr.close()

