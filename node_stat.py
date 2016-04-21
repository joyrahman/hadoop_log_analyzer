import sys
result={'object1':[0.0,500.0,0.0,0],\
        'object2':[0.0,500.0,0.0,0],\
        'object3':[0.0,500.0,0.0,0],\
        'object4':[0.0,500.0,0.0,0],\
        'object5':[0.0,500.0,0.0,0],\
        'object6':[0.0,500.0,0.0,0],\
        'object7':[0.0,500.0,0.0,0],\
        'object8':[0.0,500.0,0.0,0]}



def main(file_name):

    with open (file_name,'r') as f:
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

        print "node_name,\tmax,\t\tmin,\tavg"

        for key,value in result.items():
            result[key][2] = result[key][2]/result[key][3]
            print "{},\t{},\t\t{},\t{}".format(key,result[key][0], result[key][1],result[key][2])





if __name__=="__main__":
    main(sys.argv[1])
