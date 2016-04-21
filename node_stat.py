import sys
result={}
def main(file_name):

    with open (file_name,'r') as f:
        for line in f:
            data = line.split('@')
            #print data
            print data[0],data[6], data[10].rstrip('\n')
            key = data[6]
            value = float(data[10].rstrip('\n'))
            if key in result.keys():
                if value>result[key]:
                    result[key]=value
                    print "keyexist"
            else:
                result[key]=value



if __name__=="__main__":
    main(sys.argv[1])
    print(result)