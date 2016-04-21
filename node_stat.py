import sys
def main(file_name):

    with open (file_name,'r') as f:
        line = f.readline()
        print line


if __name__=="__main__":
    main(sys.argv[1])