import sys
import os
result={
		'object1':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object2':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object3':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object4':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object5':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object6':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object7':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object8':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0]}


header = {}


def build_header(file_name):
    #print file_name
    data = file_name.split('_')
    header['benchmark'] = data[0].rsplit('/',1)[1]
    header['file_size'] = data[1]
    header['job_id'] = data[2]
    with open(file_name,'r')as f:
        for line in f:
            #print line
            if "Job started:" in line:
                header['start'] = line.split('Job started: ')[1].rstrip('\n')
            if "Job ended: " in line:
                header['end'] = line.split('Job ended: ')[1].rstrip('\n')




def build_hadoop_data(file_name):

    with open(file_name,'r') as f:
        f.readline()
        for line in f:
            data = line.split('@')
            if (data[10]=='duration'):
                continue
            #print data
            #print data[0],data[6], data[10].rstrip('\n')

            key = data[6]
            value = float(data[10])
            if key in result.keys():
                #max
                if value>result[key][0]:
                    result[key][0]=value
                #min
                if value<result[key][1]:
                    result[key][1]=value
                #avg
                result[key][2] += value
                result[key][3] +=1

            else:
                print "keynot found"
    for key, value in result.items():
        result[key][2] = result[key][2] / result[key][3]

    # print "node_name,\tmax,\t\tmin,\tavg,\t#sessions"

    # for key, value in result.items():
    #     result[key][2] = result[key][2] / result[key][3]
    #     result[key][4] = result[key][4] / total_item
    #     result[key][4] = result[key][4] / total_item
    #     result[key][4] = result[key][4] / total_item
    #     result[key][4] = result[key][4] / total_item
    #     result[key][4] = result[key][4] / total_item
    #
    #     print "{},\t{},\t\t{},\t{}\t{}".format(key, result[key][0], result[key][1], result[key][2], result[key][3])



def print_data():
    print "--------------------------------------------"
    print "{},{},{},{},{},".format(header['job_id'],header['benchmark'],header['file_size'],header['start'],header['end'])
    print "node_name,\tmax,\tmin,\tavg,\t#sessions,\tcpu_user,\tcpu_system,\tio_wait,\tio_read,\tio_write,\tawait "
    for key, value in result.items():
        print "{},\t{},\t{},\t{},\t{},\t{},\t{},\t{},\t{},\t{},\t{}".format(key, result[key][0], result[key][1], result[key][2], result[key][3],result[key][4], \
                                                                              result[key][5], result[key][6], result[key][7], result[key][8], result[key][9])
    print "--------------------------------------------"



def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]



def build_iostat_data(file_name):

    key = "null"
    total_item = 0.0
    with open(file_name, 'r') as f:
        # time_stamp,cpu_user,cpu_system,io_wait,io_read,io_write,await,util,node_name
        #         ,    4   ,     5    ,  6     , 7    ,   8     , 9
        f.readline()

        for line in f:
            data = line.split(',')
            #print data
            key = data[8].rstrip('\n')
            result[key][4] += float(data[1])
            result[key][5] += float(data[2])
            result[key][6] += float(data[3])
            result[key][7] += float(data[4])
            result[key][8] += float(data[5])
            result[key][9] += float(data[6])
            total_item += 1
        for i in range(4,10):
            result[key][i] = result[key][i] / total_item




if __name__=="__main__":
    #main(sys.argv[1],sys.argv[2])
    # python node_stat.py <dir_name>
    if sys.argv<1:
        print "python node_stat.py <dir_name>"
        sys.exit()
    dir_path=sys.argv[1]
    listdir = listdir_fullpath(dir_path)

    for file_name in listdir:

        print "[ processing {}]".format(file_name)
        #os.path.join(__file__,'data',file_name)
        if "object" in file_name:
            build_iostat_data(file_name)
        elif "csv" in file_name:
            build_hadoop_data(file_name)
        else:
            build_header(file_name)

    #print result
    print_data()

        #print (file_name)
