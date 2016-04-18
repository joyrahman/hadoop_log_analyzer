#!/bin/python
import collections
import re
import sys
from collections import OrderedDict
from datetime import datetime
import os


#global vars
data=OrderedDict()
#data_format#
# (container_id, app_attempt) [task_no, task_creation, task_start , taask finish, host_node, task_status]


def print_data(data):
    print "[printing data]"
    for key,value in data.iteritems():
        print (key, value)
def get_attempt_id(line):
    at = line.split('appattempt_')[1].rstrip('\n')
    return at



def get_node_name(line):
    return line.split('NodeId: ')[1].split(':')[0]
    
def get_task_status(line):
    return line.split('RESULT=')[1].split('\t')[0]
    
def export_to_csv(data,file_name):
    file_extension = ".csv"
    output_dir, output_file = file_name.rsplit('/', 1)
    output_file = output_file + file_extension
    header = "container_id,attempt_id,container_no,creation_time,start_time,end_time,node,status\n"
    output_file_loc = os.path.normpath(os.path.join(output_dir,output_file))
    print "----[python hadoop module]----"
    print "output_file: {}".format(output_file_loc)
    with open(output_file_loc,'w') as f:
        f.write(header)
        for k, v in data.items():
            line = "{},{},".format(k[0],k[1])
            for item in v:
                line += str(item) + ','
            line = line[:-1] #remove trail comma    
            f.write(line+'\n')
    
            
def strip_time(line):
    return line.split(' ')[1]

def get_container_id(line):
    container_id =  line.split("container_")[1].split(' ')[0].rstrip(',')
    container_no = (container_id.split("_")[3]).lstrip('0')
    return container_id, container_no
    


def get_os_file_name(file_name):
    #file_loc = os.path.normpath(os.path.join(os.path.dirname(__file__),file_name))

    return file_name


def convert_time(e,s):
    # 22:40:11,178
    FMT = '%H:%M:%S,%f'
    tdelta = datetime.strptime(e, FMT) - datetime.strptime(s, FMT)
    seconds = tdelta.total_seconds()
    return seconds


def main(file_name, app_id):
    # step1: open the file
    # step2: search for the app_id provided
    # step3: extract app metrices
    # step4: extract container metrices
    # output to csv file
    # output to json file
    jobfound = False
    parser_start_str="Storing application with id application_{}".format(app_id)
    parser_end_str="ApplicationSummary: appId=application_{}".format(app_id)
    #parser_job_accept="application_{} State change from SUBMITTED to ACCEPTED".format(app_id)
    #parser_container_start="RESULT=SUCCESS	APPID=application_{}	CONTAINERID".format(app_id)
    #parser_container_creation   = "resourcemanager.rmcontainer.RMContainerImpl: container_"
    parser_container_creation = "Container Transitioned from NEW to ALLOCATED"
    parser_container_launch     = "LeafQueue: assignedContainer"
    parser_app_attempt_start    = "ApplicationMasterService: Registering app attempt : appattempt"
    parser_container_run        = "Container Transitioned from ACQUIRED to RUNNING"
    parser_container_finish     = "Completed container: container_"
    #parser_container_status     = "RMAuditLogger: USER=cloudsys	OPERATION=AM Released Container	TARGET=SchedulerApp	RESULT"

    #print "searching for {}".format(parser_end_str)
    with open(get_os_file_name(file_name),'r') as f:
        job_end_time = 0
        job_start_time = 0
        an = 0

        for line in f:
            #before end
            if jobfound is True and parser_end_str in line:
                job_end_time = strip_time(line)
                print "endtime:{}".format(job_end_time)
                total_duration = convert_time(job_end_time, job_start_time)
                print total_duration

                break
            #1 at the beginning
            if parser_start_str in line:
                #print line
                jobfound = True;
                job_start_time = strip_time(line)
                print "starttime:{}".format(job_start_time)

            #2 get the app aptemp number
            elif jobfound is True and parser_app_attempt_start in line:
                an = get_attempt_id(line)        
            
            #3 init the container details
            elif jobfound is True and parser_container_creation in line:
                ct = strip_time(line)    #container assign time
                tid,tn = get_container_id(line) #container_id
                st = 0  #start time
                et = 0  #end time
                nn = 0  #node_name
                ts = 0  #task_status
                #print tn,ct
                data[tid,an]=[tn,ct,st,et,nn,ts]
                
            elif jobfound is True and parser_container_launch in line:
                #print "launch_Stage"
                tid,tn = get_container_id(line)
                #st = strip_time(line)
                nn = get_node_name(line)
                #print st+nn
                #data[tid,an][2] = st
                if (tid, an) in data.keys():
                    data[tid,an][4] = nn
                
            elif jobfound is True and parser_container_run in line:
                tid,tn = get_container_id(line)
                st = strip_time(line)
                if (tid, an) in data.keys():
                    data[tid,an][2] = st
                #print tn,st 
                    
            elif jobfound is True and parser_container_finish in line:
                 tid,tn = get_container_id(line)
                 et = strip_time(line)
                 line = f.next()
                 ts = get_task_status(line)
                 print tid, an
                 if (tid,an) in data.keys():
                    data[tid,an][3] = et
                    data[tid,an][5] = ts

                # move the filepoint two lines
                #line2 = f.next()
                #line3 = f.next()
                #an = get_attempt_id(line3)
                
                #print d
                
                #print line2
                #print line3
            

            #elif jobfound is True and  parser_cotainer_details in line:
            #    line2 = f.nextline()
            #    line3 = f.nextline()
            #    print line2
            #    print line3
                #tn=((int(line.split( )[7].split('_')[4].strip('\''))))
                #st=line.split(',')[0]
                #nn=line.split()[13].split(':',1)[0].split('_')[1].split('vm')[1]
                #an=((int(line.split( )[7].split('_')[5].strip('\''))))
                #et=0
                #tn: task number
                #an: task attempt number
                #et: task finish time
                #st: task start time
                #nn: node number
                #0: task success
                #1: task killed
                #d[tn,an]=[et,st,nn,0]
                #task_no, task_attempt, task_start , taask finish, host_node, task_status







if __name__=="__main__":
    print  sys.argv
    if len(sys.argv) < 3:
        print "provide <yarn_rm_file_name> <log_file_name> <job_id>";
        sys.exit();
    file_name = sys.argv[2]
    yarn_rm_file_name = sys.argv[1]
    app_id = sys.argv[3]
    main(yarn_rm_file_name, app_id)
    print_data(data)

    export_to_csv(data, file_name)


# python hadoop_perser.py /home/cloudsys/hadoop/logs/yarn-cloudsys-resourcemanager-proxy.log /home/cloudsys/hadoop_log/wordcount_4M_7899682 1460750106009


#test
#  application_1455576005827_0001
#  app__1455576005827.java