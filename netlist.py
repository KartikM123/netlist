import sys, getopt

def main (argc, argv):
    try:
        opts, args = getopt.getopt(argv, "h:i", ["--pull"])
    except:
        print("error")
        return 1
    for opt, arg in opts:
        print (opt,arg)
    return

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)