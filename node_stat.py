import sys
def main(file_name):

    with open (file_name,'r') as f:
        for line in f.readline():
            line = line.split('@)
            print line[0],line[6],line[8]


if __name__=="__main__":
    main(sys.argv[1])