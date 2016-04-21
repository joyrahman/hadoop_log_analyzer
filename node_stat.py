import sys
def main(file_name):

    with open (file_name,'r') as f:
        for line in f.readline():
            data = line.split('@')
            print data[0],data[6]


if __name__=="__main__":
    main(sys.argv[1])