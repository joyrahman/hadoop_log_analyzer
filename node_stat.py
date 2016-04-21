import sys
result={}
def main(file_name):

    with open (file_name,'r') as f:
        f.readline()
        for line in f:
            data = line.split('@')
            if (data[10]=='duration'):
                continue
            #print data
            print data[0],data[6], data[10].rstrip('\n')

            key = data[6]
            value = float(data[10])
            if key in result.keys():
                if value>result[key]:
                    result[key]=value
                    print "keyexist"
            else:
                result[key]=value



if __name__=="__main__":
    main(sys.argv[1])
    print(result)