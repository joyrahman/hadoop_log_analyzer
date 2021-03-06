#!/bin/python
import collections
import re
import sys
from collections import OrderedDict
#from datetime import datetime
import datetime
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
    return "NA"
    #return line.split('EVENT=')[1].split('\t')[0]
    
def export_to_csv(data,file_name):
    #print data
    file_extension = ".csv"
    output_dir, output_file = file_name.rsplit('/', 1)
    output_file = output_file + file_extension
    header = "container_id,container_no,application_id,attempt_id,start_time,end_time,node_name,cpu_alloc,memory_alloc,container_status,duration\n"
    output_file_loc = os.path.normpath(os.path.join(output_dir,output_file))
    #print "----[python hadoop module]----"
    print "output_file: {}".format(output_file_loc)
    with open(output_file_loc,'w') as f:
        f.write(header)
        for k, v in data.items():
            #line = "{},{},".format(k[0],k[1])
            line = "{},".format(k)
            i = 0
            for item in v:
                if(i==4 or i==5):
                    line += "{}".format(str(item)) + ','
                else:
                    line += str(item) + ','
                i+=1
            line = line[:-1] #remove trail comma    
            f.write(line+'\n')
            print line

    
            
def strip_time(line):
    return line.split(' ')[1]

def get_container_id(line):
    '''
    application_1460750106009_0001
        appattempt_1460750106009_0001_000001
            container_1460750106009_0001_01_000001
            container_1460750106009_0001_02_000001

    '''

    container_id =  line.split("container_")[1].split(' ')[0].rstrip(',')

    attempt_id =    line.split("appattempt_")[1].split(' ')[0].rstrip(',')
    application_id = (container_id.split("_")[0]) +"_"+ (container_id.split("_")[1])
    container_no = (attempt_id.rsplit("_",1)[1]).lstrip('0') + "_" +(container_id.split("_")[3]).lstrip('0')

    return container_id, container_no,application_id, attempt_id
    


def get_os_file_name(file_name):
    #file_loc = os.path.normpath(os.path.join(os.path.dirname(__file__),file_name))

    return file_name


def convert_time(e,s):
    # 22:40:11,178
    FMT = '%H:%M:%S.%f'
    tdelta = datetime.datetime.strptime(e, FMT) - datetime.datetime.strptime(s, FMT)
    seconds = tdelta.total_seconds()
    return seconds

def get_resource_allocated(line):
    cpu,mem=0,0
    extract_line = line.split("Resource:",1)[1].split(">,",1)[0]
    mem_data = extract_line.split(', ')[0].split('memory:')[1].rstrip(',')
    cpu_data = extract_line.split(', ')[1].split('vCores:')[1].rstrip(',')

    return cpu_data,mem_data



def get_task_status(line):
    status = line.split('with event:')[1].rstrip('\n')
    return  status

def main(file_name, app_id):
    # step1: open the file
    # step2: search for the app_id provided
    # step3: extract app metrices
    # step4: extract container metrices
    # output to csv file
    # output to json file
    jobfound = False

    local_time = datetime.datetime.now()
    utc_time  = datetime.datetime.utcnow()
    time_delta = utc_time.hour - local_time.hour

    print ("running on:",app_id)

    #LeafQueue: assignedContainer application attempt=appattempt_1460750106009_0001_000002 container=Container: [ContainerId: container_1460750106009_0001_02_000001, NodeId: object4:42773, NodeHttpAddress: object4:8042, Resource: <memory:2048, vCores:1>, Priority: 0, Token: null, ] queue=default: capacity=1.0, absoluteCapacity=1.0, usedResources=<memory:0, vCores:0>, usedCapacity=0.0, absoluteUsedCapacity=0.0, numApps=1, numContainers=0 clusterResource=<memory:65536, vCores:64>
    parser_container_creation   = "LeafQueue: assignedContainer application"
    parser_container_finish     = "released container container_"
    #parser_container_status     = "RMAuditLogger: USER=cloudsys	OPERATION=AM Released Container	TARGET=SchedulerApp	RESULT"
    #CapacityScheduler: Application attempt appattempt_1460750106009_0001_000002 released container container_1460750106009_0001_02_000001 on node: host: object4:42773 #containers=0 available=<memory:8192, vCores:8> used=<memory:0, vCores:0> with event: KILL

    #print "searching for {}".format(parser_end_str)
    with open(get_os_file_name(file_name),'r') as f:

        for line in f:

            if parser_container_creation in line and app_id in line:
                #print("[Debug:{}]{}".format(app_id,line))
                container_id, container_no,application_id, attempt_id  = get_container_id(line)
                #start_time = "{}".format(strip_time(line))
                start_time = datetime.datetime.strptime(strip_time(line), "%H:%M:%S,%f")
                start_time = start_time - datetime.timedelta(hours=time_delta)
                start_time_string = "{}:{}:{}.{}".format(start_time.hour, start_time.minute, start_time.second, start_time.microsecond)
                #end_time= datetime.datetime.now()
                end_time = start_time
                end_time_string = start_time_string
                duration=0
                node_name = get_node_name(line)
                cpu_alloc,memory_alloc = get_resource_allocated(line)
                container_status = "NA"
                data[container_id]=[container_no,application_id,attempt_id,start_time_string,end_time_string,node_name,cpu_alloc,memory_alloc,container_status,duration]
                #print "[debug:]",line

                    
            elif parser_container_finish in line and app_id in line:
                 print "[debug:]",line
                 container_id = get_container_id(line)[0]
                 #end_time = "{}".format(strip_time(line))
                 end_time = datetime.datetime.strptime(strip_time(line), "%H:%M:%S,%f")
                 end_time = end_time - datetime.timedelta(hours=time_delta)
                 end_time_string = "{}:{}:{}.{}".format(end_time.hour, end_time.minute, end_time.second, end_time.microsecond)

                 container_status = get_task_status(line)
                 if container_id in data.keys():
                    data[container_id][4] = end_time_string
                    data[container_id][8] = container_status
                    data[container_id][9] = convert_time(end_time_string , data[container_id][3])






if __name__=="__main__":
    #print  sys.argv
    if len(sys.argv) < 3:
        print "provide <yarn_rm_file_name> <log_file_name> <job_id>"
        sys.exit()
    file_name = sys.argv[2]
    yarn_rm_file_name = sys.argv[1]
    app_id = sys.argv[3]
    main(yarn_rm_file_name, app_id)
    #print_data(data)

    export_to_csv(data, file_name)


# python hadoop_perser.py /home/cloudsys/hadoop/logs/yarn-cloudsys-resourcemanager-proxy.log /home/cloudsys/hadoop_log/wordcount_4M_7899682 1460750106009


#test
#  application_1455576005827_0001
#  app__1455576005827.java