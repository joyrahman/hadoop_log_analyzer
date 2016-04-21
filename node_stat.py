import sys
result={
		'object1':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object2':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object3':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object4':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object5':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object6':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object7':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0],\
        'object8':[0.0,500.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0]}



def build_hadoop_data(file_name):

    with open (file_name1,'r') as f:
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




def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]



def build_iostat_data(file_name):

    key = "null"
    total_item = 0
    with open(file_name2, 'r') as f:
        # time_stamp,cpu_user,cpu_system,io_wait,io_read,io_write,await,util,node_name
        #         ,    4   ,     5    ,  6     , 7    ,   8     , 9
        f.readline()

        for line in f:
            data = line.split()
            key = data[8]
            result[key][4] += data[1]
            result[key][5] += data[2]
            result[key][6] += data[3]
            result[key][7] += data[4]
            result[key][8] += data[5]
            result[key][9] += data[6]
            total_item += 1
        for i in range(4,10):
            result[key][i] = result[key][i] / total_item




if __name__=="__main__":
    #main(sys.argv[1],sys.argv[2])
    # python node_stat.py <dir_name>
    if sys.argv<1:
        print "python node_stat.py <dir_name>"
        sys.exit()
    dir_path=sys.argv[2]
    listdir = listdir_fullpath(dir_path)

    for file_name in listdir:

        print file_name
        #os.path.join(__file__,'data',file_name)
        if "object" and "csv" in file_name:
            build_iostat_data(file_name)
        else if "csv" in file_name:
            build_hadoop_data(file_name)

    print result
        #print (file_name)
