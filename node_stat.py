import sys
def main(file_name):

    with open (file_name,'r') as f:
        for line in f:
            data = line.split('@')
            #print data
            print data[0],data[6],data[10].rstrip('\n')


if __name__=="__main__":
    main(sys.argv[1])