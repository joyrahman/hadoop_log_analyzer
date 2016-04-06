#!/bin/python
import collections
import re
import sys
from collections import OrderedDict
from datetime import datetime
import os


#global vars
d=OrderedDict()
#data_format#
# app_attempt, task_no, task_start , taask finish, host_node, task_status

def get_strip_time(date_string):
    return date_string.split(' ')[1]

def get_container_id(data):
    return data.split("CONTAINERID=")[1]


def get_os_file_name(file_name):
    file_loc = os.path.normpath(os.path.join(os.path.dirname(__file__),file_name))
    return file_loc


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
    parser_job_accept="application_{} State change from SUBMITTED to ACCEPTED".format(app_id)
    parser_container_start="RESULT=SUCCESS	APPID=application_{}	CONTAINERID".format(app_id)
    parser_cotainer_details=" container=Container: [ContainerId:"



    print "searching for {}".format(parser_end_str)
    with open(get_os_file_name(file_name),'r') as f:
        for line in f:
            if jobfound is True and parser_end_str in line:
                job_end_time = get_strip_time(line)
                print "endtime:{}".format(job_end_time)
                total_duration = convert_time(job_end_time,job_start_time)
                print total_duration

                break
            if parser_start_str in line:
                jobfound = True;
                job_start_time = get_strip_time(line)
                print "starttime:{}".format(job_start_time)

            elif parser_container_start in line:
                container_start_time = get_strip_time(line)
                container_id = get_container_id(line)
                print container_id + container_start_time
                line2 = f.next()
                line3 = f.next()
                #print line2
                print line3

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
    if len(sys.argv) < 3:
        print "provide <file_name> <job_id>";
        sys.exit();
    file_name = sys.argv[1]
    app_id = sys.argv[2]
    main(file_name, app_id)



#test
#  application_1455576005827_0001
#  app__1455576005827.java