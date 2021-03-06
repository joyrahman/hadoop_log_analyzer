import collections
import re
from collections import OrderedDict
from datetime import datetime
from itertools import islice
import os
import sys
import csv



#fout2 = open("data2.txt",'w');
#fout3 = open("data3.txt",'w');
#fout4 = open("data4.txt",'w');
#fout5 = open("data5.txt",'w');
#fout6 = open("data6.txt",'w');
#fout7 = open("data7.txt",'w');

def extract_node_name(file_name):
    #iostat_log_name="${hadoop_benchmark}_object${j}_${hadoop_file_size}_${job_id}"
    #benchmarkname_node_appid_st_et
    file_name = file_name.rsplit('/',1)[1]
    header = {}
    header['benchmark'] = file_name.split('_')[0]
    header['node'] = file_name.split('_')[1]
    header['size'] = file_name.split('_')[2]
    header['appid']    = file_name.split('_')[3]
    return header


def write_to_csv(csv_data,file_name):
    #file_extension = ".csv"
    #output_file = file_name.split('.')[0]+ file_extension
    header = "time_stamp,cpu_user,cpu_system,io_wait,io_read,io_write,await,util,node_name\n"
    #output_file_loc = os.path.normpath(os.path.join(os.path.dirname(__file__),output_file))
    print "output file: " + file_name

    with open(file_name, 'wa') as fp:
        #header = "ts,user,system,iowait,read,write,await,svc,util"
        #fp.write(header)
        #fp.write("\n")
        fp.write(header)
        for rows in csv_data:
            if rows.has_key('ts') and rows.has_key('read'):
                line = rows['ts'] +","+ rows['user'] +","+ rows['system'] +","+ rows['iowait'] +","+ rows['read'] +"," + rows['write'] +","+ rows['await'] +","+ rows['util'] +"," + rows['node'] +  '\n'
                fp.write(line)
                #fp.write('\n')
        #a = csv.writer(fp, delimiter=',')
        #a.writerows(csv_data)



def main(command_param):
    input_file_name=command_param[0]
    #file_loc = os.path.normpath(os.path.join(os.path.dirname(__file__),input_file_name))
    #output_file_name = input_file_name.split('.')[0]
    output_file_name = command_param[1]
    header = extract_node_name(input_file_name)
    print "input file: " + input_file_name
    global_data = []
    
    with open(input_file_name,"r") as f:
        lines_after_48 = f.readlines()[2:]
        
        M=0
        N = 7
        #init val was 157
        while(N<500):
            lines_gen = islice(lines_after_48, M,N)
            #print "------------------------------"
            #print (lines_gen)
            data = {}
            for i, line in enumerate(lines_gen):
                #print "i:"+str(i)
                #print (line)
                #node=line.split()[0].split(':',1)[0].split('object')[1]
                ts = 0
                user=0
                system=0
                iowait=0
                read=0
                write=0
                await=0
                svc=0
                util=0
                #firt line with time stamp
                if i == 0:
                    ts=line.split()
                    #tm = datetime.strptime(line, "%m/%d/%Y %I:%M:%S %p")
                    data['ts'] = ts[1]
                    data['node'] = header['node']
                    data['benchmark'] = header['benchmark']
                    data['size'] = header['size']
                    data['appid'] = header['appid']
                    
                #third line with cpu utilizaiton     
                if i == 2:
                    #print str(i) + ">" +line
                    user=line.split( )[0]
                    system=line.split( )[2]
                    iowait=line.split( )[3]
                    steal =line.split( )[4]
                    idle = line.split( )[5]
                    #if node=="2" and user!='' and system!='' and iowait!='':
                    #    fout2.write(str(user)+","+str(system)+","+str(iowait)+",")
                    #elif node=="3" and user!='' and system!='' and iowait!='':
                    #    fout3.write(str(user)+","+str(system)+","+str(iowait)+",")
                    #elif node=="4" and user!='' and system!='' and iowait!='':
                    #    fout4.write(str(user)+","+str(system)+","+str(iowait)+",")
                    #elif node=="5" and user!='' and system!='' and iowait!='':
                    #    fout5.write(str(user)+","+str(system)+","+str(iowait)+",")
                    #elif node=="6" and user!='' and system!='' and iowait!='':
                    #    fout6.write(str(user)+","+str(system)+","+str(iowait)+",")
                    #elif node=="7" and user!='' and system!='' and iowait!='':
                    #    fout7.write(str(user)+","+str(system)+","+str(iowait)+",")
                    data['user'] = user
                    data['system'] = system
                    data['iowait'] = iowait
                if i == 5:
                    #['Device:', 'rrqm/s', 'wrqm/s', 'r/s',  'w/s', 'rMB/s', 'wMB/s', 'avgrq-sz', 'avgqu-sz', 'await', 'r_await', 'w_await', 'svctm', '%util']
                    #['sda',      '0.00' ,  '4.40' , '0.00', '1.20', '0.00', '0.03' , '52.00'   , '0.00'     , '0.67', '0.00'   , '0.67'   , '0.67' , '0.08']

                    #pass
                    #print line
                    #print str(i) + ">" +line
                    data['read']=line.split( )[5]
                    data['write']=line.split( )[6]
                    data['await']=line.split( )[9]
                    #data['svc']=line.split( )[12]
                    data['util']=line.split( )[13]
                    #if node=="2" and read!='' and write!='' and await!='' and svc!='' and util!='':
                    #    fout2.write(str(read)+","+str(write)+","+str(await)+","+str(svc)+","+str(util)+"\n")
                    #elif node=="3" and read!='' and write!='' and await!='' and svc!='' and util!='':
                    #    fout3.write(str(read)+","+str(write)+","+str(await)+","+str(svc)+","+str(util)+"\n")
                    #elif node=="4" and read!='' and write!='' and await!='' and svc!='' and util!='':
                    #    fout4.write(str(read)+","+str(write)+","+str(await)+","+str(svc)+","+str(util)+"\n")
                    #elif node=="5" and read!='' and write!='' and await!='' and svc!='' and util!='':
                    #    fout5.write(str(read)+","+str(write)+","+str(await)+","+str(svc)+","+str(util)+"\n")
                    #elif node=="6" and read!='' and write!='' and await!='' and svc!='' and util!='':
                    #    fout6.write(str(read)+","+str(write)+","+str(await)+","+str(svc)+","+str(util)+"\n")
                    #elif node=="7" and read!='' and write!='' and await!='' and svc!='' and util!='':
                    #    fout7.write(str(read)+","+str(write)+","+str(await)+","+str(svc)+","+str(util)+"\n")
                    
            #print data
            global_data.append(data)
            M=M+7
            N=N+7
    write_to_csv(global_data, output_file_name)
#fout2.close()
#fout3.close()
#fout4.close()
#fout5.close()
#fout6.close()
#fout7.close()

#file name format
# benchmarkname_node_appid_st_et
                
if __name__ == "__main__":
    if len(sys.argv)>1:
        main(sys.argv[1:])
    else:
        print "<exec_name> <input_file_name: wordcount2_object7_111> <output_file>"
        